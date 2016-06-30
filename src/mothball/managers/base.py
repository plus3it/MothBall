import abc
import time
import json
import boto3
import logging

from mothball.managers.services import InstanceManager, SecurityGroupManager, EBSManager, EIPManager
from mothball.db.managers.base import RDSManager, DBManager


class AWSManager(object):

    def __init__(self, region, key, secret, username, password, dbname,
                 host, port, db_type, dry_run=True, rds_db=True, rds_name=None, *vpc_sg):
        # type: str, str, str

        self.region = region
        self.key = key
        self.secret = secret
        self.username = username
        self.password = password
        self.dbname = dbname
        self.db_type = db_type
        self.host = host
        self.port = port
        self.ec2_instances = None
        self.ec2_session = None
        self.data = dict()
        self.vpc_sg = vpc_sg
        self.rds_db = rds_db
        self.db_session = None
        self.rds_name = rds_name
        self.dry_run = dry_run

        self.Session = boto3.Session(
            region_name=self.region,
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret
            )

    def _get_ec2_session(self):

        if not self.ec2_session:
            self.ec2_session = self.Session.resource('ec2',
                                                     region_name=self.region,
                                                     aws_access_key_id=self.key,
                                                     aws_secret_access_key=self.secret)
        else:
            logging.warning('EC2 Session already exists.  Using existing Session.')

    def _validate_ec2_region(self):

        ec2 = boto3.client('ec2')
        regions = ec2.describe_regions()

        if not any(k['RegionName'] for k in regions['Regions'] if self.region == k['RegionName']):
            return False

    def _get_ec2_instances(self):

        if not self.ec2_session:
            self._get_ec2_session()

        instlist = [instance.id for instance in self.ec2_session.instances.all()]

        self.ec2_instances = instlist

    def _create_tables(self):

        if not self.db_session:
            logging.info('Creating DB session.')
            self.get_db_connection()
        else:
            logging.info('DB connection already exists, reusing.')

        self.db_session.create_tables()

    def _terminate(self, instances):

        pass
        # TODO try except
        # self.ec2_session.terminate_instances(DryRun=self.dry_run,
        #                                      InstanceIds=instances)

    def get_account_info(self):

        self.iam_session = self.Session.resource('iam',
                                                    region_name=self.region,
                                                    aws_access_key_id=self.key,
                                                    aws_secret_access_key=self.secret)
        self.account_id = self.iam_session.CurrentUser().arn.split(':')[4]
        self.user_id = self.iam_session.CurrentUser().arn.split(':')[5]

    def get_db_connection(self):

        if self.rds_db:
            DB = RDSManager(self.db_type, self.rds_name, self.dbname, self.username, self.password, self.Session, self.vpc_sg)
        else:
            DB = DBManager(self.db_type, self.dbname, self.username, self.password, self.host, self.port)

        self.db_session = DB.create_db_session()
        self.db_session.connect()

    def get_info(self):

        if not self.ec2_instances:
            self._get_ec2_instances()

        eipm = EIPManager(self.ec2_session, self.db_session)
        ebsm = EBSManager(self.ec2_session, self.db_session)
        sgm = SecurityGroupManager(self.ec2_session, self.db_session)
        im = InstanceManager(self.ec2_session, self.db_session)

        # TODO check to see if tables exist?
        self._create_tables()

        mothballed_instances = list()
        for instance in self.ec2_instances:
            im.create_record(self.account_id, instance)
            sgm.create_record(self.account_id, instance)
            ebsm.create_record(self.account_id, instance, dry_run=self.dry_run)
            eipm.create_record(self.account_id, instance)
            mothballed_instances.append(instance)

        self._terminate(mothballed_instances)

    def __repr__(self):
        return "<account_info='{0}, user_id='{1}'>".format(self.account_id, self.user_id)


















