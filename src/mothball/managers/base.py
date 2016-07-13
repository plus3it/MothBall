import boto3
import logging

from mothball.managers.services import InstanceManager, SecurityGroupManager, EBSManager, EIPManager
from mothball.db.managers.base import RDSManager, DBManager


class AWSManager(object):
    """
    This is the core interface for the User's AWS Account.  It handles all interactions with AWS Services.

    """

    def __init__(self, region, key, secret, control_region, control_key, control_secret,
                 username, password, dbname, host, port, db_type, rds_db=True,
                 rds_name=None, *vpc_sg):
        """
        :param region: The region to be backedup.
        :type region: string
        :param key: The AWS key for the User's AWS account.
        :type key: string
        :param secret: The Secret key for the User's AWS account.
        :type secret: string
        :param username: The Database Username (will be created if it doesn't exist)
        :type username: basestring
        :param password: The Database Password (will be created if it doesn't exist)
        :type password: basestring
        :param dbname: The Database name.
        :type dbname: basestring
        :param host: The hostname for the database to be used or created. (Only needed if RDS is not being used)
        :type host: basestring
        :param port: The port for the database to be used or created. (Only needed if RDS is not being used)
        :type port: basestring
        :param db_type: Currently only supports MySQL and PostgreSQL
        :type db_type: basestring
        :param rds_db: If RDS should be used for housing the configuration data.
        :type rds_db: bool
        :param rds_name: The name of the RDS instance being created or used.
        :type rds_name: basestring
        :param vpc_sg: The security groups for the RDS instance to be used. (Only needed for creating RDS Instances)
        :type vpc_sg: list of basestring
        """

        self.region = region
        self.key = key
        self.secret = secret
        self.control_region = control_region
        self.control_key = control_key
        self.control_secret = control_secret
        self.username = username
        self.password = password
        self.dbname = dbname
        self.db_type = db_type
        self.host = host
        self.port = port
        self.vpc_sg = vpc_sg
        self.rds_db = rds_db
        self.rds_name = rds_name

        self.ec2_instances = None
        self.ec2_session = None
        self.db_session = None
        self.iam_session = None
        self.account_id = None
        self.user_id = None
        self.Session = None

    def _get_session(self, region, key, secret):

        Session = boto3.Session(
            region_name=self.region,
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret
            )

        return Session

    def _get_ec2_session(self):
        """
        Private method for creating an ec2 session. This interface will setup be used for collecting account an instance
        data for backups.
        """
        if not self.Session:
            self.Session = self._get_session(self.region, self.key, self.secret)

        if not self.ec2_session:
            self.ec2_session = self.Session.resource('ec2',
                                                     region_name=self.region,
                                                     aws_access_key_id=self.key,
                                                     aws_secret_access_key=self.secret)
        else:
            logging.warning('EC2 Session already exists.  Using existing Session.')

    def _get_ec2_instances(self):
        """
        Private method for getting a list of instance ids and setting the ec2_instances attribute.
        """
        if not self.ec2_session:
            self._get_ec2_session()

        instlist = [instance.id for instance in self.ec2_session.instances.all()]

        self.ec2_instances = instlist

    def _create_tables(self):
        """
        Calls the create_tables method from the correct database manager.  If a database session has not be already
        initiated it will first create the database session.
        """
        if not self.db_session:
            logging.info('Creating DB session.')
            self.get_db_connection()
        else:
            logging.info('DB connection already exists, reusing.')

        self.db_session.create_tables()

    def terminate(self, instances):
        """
        Terminates ec2 instances.

        :param instances: The ec2 instances that will be terminated.
        :type instances: list of strings
        """
        ec2_client = self.Session.client('ec2',
                                         region_name=self.region,
                                         aws_access_key_id=self.key,
                                         aws_secret_access_key=self.secret)

        for instance in instances:
            print('Terminating instance {0}'.format(instance))

        ec2_client.terminate_instances(DryRun=False,
                                           InstanceIds=instances)
            # TODO this returns JSON data of the terminated instances, it should be pushed into the DB


    def get_account_info(self):
        """
        Gets the account information for the User's account and sets object attributes with the necessary data. This
        information will be used for the Mothball backup application. It creates attribute with iam session,
        account_id, and user_id.
        """
        if not self.Session:
            self.Session = self._get_session(self.region, self.key, self.secret)

        self.iam_session = self.Session.resource('iam',
                                                 region_name=self.region,
                                                 aws_access_key_id=self.key,
                                                 aws_secret_access_key=self.secret)
        self.account_id = self.iam_session.CurrentUser().arn.split(':')[4]
        self.user_id = self.iam_session.CurrentUser().arn.split(':')[5]

    def get_db_connection(self):
        """
        Creates a database connection depending on the location (RDS/NonRDS) and sets the db_session attribute on the
        object for database access.
        """
        if self.rds_db:
            self.home_session = self._get_session(self.control_region, self.control_key, self.control_secret)
            db = RDSManager(self.db_type, self.rds_name, self.dbname, self.username, self.password, self.home_session,
                            self.vpc_sg)
        else:
            db = DBManager(self.db_type, self.dbname, self.username, self.password, self.host, self.port)

        self.db_session = db.create_db_session()
        self.db_session.connect()

    def get_instances(self):
        if not self.ec2_instances:
            self._get_ec2_instances()

        return self.ec2_instances

    def backup_instances(self):
        """
        Main cadence for backing up instance data to a database. It collects all of the instance ids for a region first.
        It then creates a manager for each configuration set that is being backed up. After creating the managers it
        creates a record for each instance configuration set and records the instance id.

        :return: The instances that configuration data was backed up.
        :rtype: list of strings
        """
        if not self.ec2_instances:
            self._get_ec2_instances()

        eipm = EIPManager(self.ec2_session, self.db_session)
        ebsm = EBSManager(self.ec2_session, self.db_session)
        sgm = SecurityGroupManager(self.ec2_session, self.db_session)
        im = InstanceManager(self.ec2_session, self.db_session)

        # TODO check to see if tables exist?
        self._create_tables()

        for instance in self.ec2_instances:
            im.create_record(self.account_id, instance)
            sgm.create_record(self.account_id, instance)
            ebsm.create_record(self.account_id, instance)
            eipm.create_record(self.account_id, instance)

    def create_snapshots(self):

        if not self.ec2_instances:
            self._get_ec2_instances()

        ebsm = EBSManager(self.ec2_session)

        for instance in self.ec2_instances:
            ebsm.snapshot_volumes(instance)

    def __repr__(self):
        """
        Returns attribute data currently set for the AWSManager Object.
        :return:
        """
        return "<account_info='{0}, user_id='{1}'>".format(self.account_id, self.user_id)


















