import abc
import time
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mothball.db.models.base import Base


class DBManager(object):
    """
    Interface for non-RDS databases.
    """

    def __init__(self, db_type, dbname, username, password, host, port):
        """
        :param db_type: Currently only supports MySQL and PostgreSQL
        :type db_type: string
        :param dbname: Name of the Database to be used.
        :type dbname: string
        :param username: The Database Username (will be created if it doesn't exist)
        :type username: string
        :param password: The Database Password (will be created if it doesn't exist)
        :type password: string
        :param host: The hostname for the database to be used or created. (Only needed if RDS is not being used)
        :type host: string
        :param port: The port for the database to be used or created. (Only needed if RDS is not being used)
        :type port: string
        """
        self.db_type = db_type
        self.dbname = dbname
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def create_db_session(self):
        """
        Create the database session.

        :return: Database session interface.
        :rtype: Database Session Object
        """
        dbsession = SQLConnect(self.host,
                               self.port,
                               dbname=self.dbname,
                               username=self.username,
                               password=self.password,
                               db_type=self.db_type
                               )

        return dbsession


class RDSManager(object):
    """
    Interface for RDS databases.
    """

    def __init__(self, db_type, name, dbname, username, password, awssession, vpc_sg):
        """
        :param db_type: Currently only supports MySQL and PostgreSQL
        :type db_type: string
        :param name: RDS name
        :type name: string
        :param dbname: Name of the Database to be used.
        :type dbname: string
        :param username: The Database Username (will be created if it doesn't exist)
        :type username: string
        :param password: The Database Password (will be created if it doesn't exist)
        :type password: string
        :param awssession: The interface for the aws ec2 session.
        :type awssession: EC2 Session Object
        :param vpc_sg: The security groups that should be applied to the RDS Instance.
        :type vpc_sg: list of strings
        """
        self.db_type = db_type
        self.name = name
        self.dbname = dbname
        self.username = username
        self.password = password
        self.Session = awssession
        self.vpc_sg = vpc_sg
        self.instance_info = None
        self.rds_session = None

    def _check_rds_instance_exists(self):
        """
        Private method to check to see if an RDS Instance already exists for the name that was given.

        :return: Validation if an RDS Instance exists with the supplied name.
        :rtype: bool
        """
        return any(k for k in self.rds_session.describe_db_instances()['DBInstances']
                   if k['DBInstanceIdentifier'] == self.name.lower())

    def _get_rds_db_info(self):
        """
        Private method to collect the RDS Instance info. Sets the instance_info attribute with the configuration
         information for the RDS Instance.
        """
        for instance in self.rds_session.describe_db_instances()['DBInstances']:
            if instance['DBInstanceIdentifier'] == self.name.lower():
                self.instance_info = instance

    def _create_rds_instance(self):
        """
        Private method to create the RDS Instance. If the instance is created, it will loop until it the instance is
        available to be used so that the application can continue.
        """
        if self.db_type.lower() != 'mysql':
            version = '9.5'
        else:
            version = '5.7'

        self.rds_session.create_db_instance(DBInstanceIdentifier=self.name,
                                            AllocatedStorage=200,
                                            DBInstanceClass='db.t2.micro',
                                            DBName=self.dbname,
                                            Engine=self.db_type,
                                            EngineVersion=version,
                                            MasterUsername=self.username,
                                            MasterUserPassword=self.password,
                                            VpcSecurityGroupIds=self.vpc_sg
                                            )

        self._get_rds_db_info()
        while 'Endpoint' not in self.instance_info:
            time.sleep(5)
            self._get_rds_db_info()

    def create_db_session(self):
        """
        Create the RDS database session.

        :return: RDS Database session interface.
        :rtype: Database Session Object
        """
        self.rds_session = self.Session.client('rds')

        if not self._check_rds_instance_exists():
            self._create_rds_instance()
        else:
            self._get_rds_db_info()

        dbsession = SQLConnect(self.instance_info['Endpoint']['Address'],
                               self.instance_info['Endpoint']['Port'],
                               dbname=self.dbname,
                               username=self.username,
                               password=self.password,
                               db_type=self.db_type
                               )

        return dbsession


class SQLConnect(object):
    """
    Interface for database connections.
    """

    def __init__(self, address, port, dbname='AWSBackup',
                 username='mothball', password='mothballP4ssw0rd', db_type='managers'):

        self.dbname = dbname
        self.username = username
        self.password = password
        self.address = address
        self.port = port
        self.session = None
        self.db_type = db_type
        self.engine = None
        self.session = None

    # TODO breakout Mysql and Postgres to child classes that import SQLConenct (DBBase?)

    def _mysql(self):
        self.engine = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(self.username,
                                                                                 self.password,
                                                                                 self.address,
                                                                                 self.port,
                                                                                 self.dbname))

    def _postgres(self):
        self.engine = create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(self.username,
                                                                              self.password,
                                                                              self.address,
                                                                              self.port,
                                                                              self.dbname))

    def _db_picker(self):
        if self.db_type == 'postgresql':
            self._postgres()
        else:
            self._mysql()

    def connect(self):

        if not self.engine:
            self._db_picker()

        Base.metadata.bind = self.engine
        dbsession = sessionmaker(bind=self.engine)
        self.session = dbsession()

    def create_tables(self):

        if not self.engine:
            self._db_picker()

        Base.metadata.create_all(self.engine)

    def close(self):
        self.session.close()

    def update(self, data_object):
        if not self.session:
            logging.warning('No db session has been made to create a record for.  self.connect first.')
        else:
            self.session.add(data_object)
            self.session.commit()
