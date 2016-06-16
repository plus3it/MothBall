import abc
import time
import json
import boto3
import logging

from mothball.db.models.base import Base, EBS, EIP
from mothball.db.managers.base import RDSManager, DBManager, SQLConnect


class AWSServiceManager(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, ec2_session, db_session):
        self.ec2_session = ec2_session
        self.db_session = db_session

    @abc.abstractmethod
    def create_record(self, account_id, instance_id, instance):
        return

class AWSManager(object):

    def __init__(self, region, key, secret, username, password, dbname, db_type, rds_db=True, *vpc_sg):
        # type: str, str, str

        import pydevd
        pydevd.settrace('108.56.149.231', port=31337, stdoutToServer=True, stderrToServer=True)

        self.region = region
        self.key = key
        self.secret = secret
        self.username = username
        self.password = password
        self.dbname = dbname
        self.db_type = db_type
        self.ec2_instances = None
        self.ec2_session = None
        self.data = dict()
        self.vpc_sg = vpc_sg
        self.rds_db = rds_db
        self.db_session = None

        self.Session = boto3.Session(
            region_name=self.region,
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret
            )

    def get_db_connection(self):

        if self.rds_db:
            DB = RDSManager(self.db_type, self.dbname, self.username, self.password, self.Session, self.vpc_sg)
        else:
            DB = DBManager(self.db_type, self.dbname, self.username, self.password, self.host, self.port)

        self.db_session = DB.create_db_session()

    def _get_ec2_session(self):

        if not self.ec2_session:
            self.ec2_session = self.Session.resource('ec2',
                                                     region_name=self.region,
                                                     aws_access_key_id=self.key,
                                                     aws_secret_access_key=self.secret)
        else:
            logging.warning('EC2 Session already exists.  Using existing Session.')

    def get_account_info(self):

        self.iam_session = self.Session.resource('iam',
                                                    region_name=self.region,
                                                    aws_access_key_id=self.key,
                                                    aws_secret_access_key=self.secret)
        self.account_id = self.iam_session.CurrentUser().arn.split(':')[4]
        self.user_id = self.iam_session.CurrentUser().arn.split(':')[5]

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

    def _create_tables(self, name='FOOOOOO'):

        if not self.db_session:
            logging.info('Creating DB session.')
            self.get_db_connection()
        else:
            logging.info('DB connection already exists, reusing.')

        self.db_session.create_tables()

    def get_info(self):

        if not self.ec2_instances:
            self._get_ec2_instances()



        for instance in self.ec2_instances:
            if instance in self.data:
                logging.warning('Instance {0} already exists in Data?'.format(instance))

            self.data[instance] = dict()
            self._get_ebs_volume_info(instance)

            self._get_eip_info(instance)

    def dump_data(self):
        if not self.data:
            self.get_info()

        self.get_account_info()

        self._create_rds_tables()

        s = SQLConnect(self.instance_info['Endpoint']['Address'],
                       self.instance_info['Endpoint']['Port'],
                       self.username,
                       self.password,
                       self.db_type
               )

        s.connect()

        for instance in self.data:
            for vol in self.data[instance]['EBS']:
                ebs = self.data[instance]['EBS'][vol]
                new_ebs = EBS()
                # new_eip = EIP()
                new_ebs.AccountId = self.account_id
                new_ebs.instanceId = instance
                new_ebs.attachmentSet = ebs.get('Mount')
                new_ebs.availabilityZone = ebs.get('AZ')
                new_ebs.createTime  = None
                new_ebs.encrypted = False
                new_ebs.iops = ebs.get('IOPS')
                new_ebs.kmsKeyId = None
                new_ebs.size = ebs.get('Size')
                new_ebs.snapshotId = None
                new_ebs.status = None
                new_ebs.volumeId = vol
                new_ebs.volumeType = ebs.get('Type')
                #new_ebs.tagSet = ebs.get('Tags')
                s.update(new_ebs)

"""
            for interface in self.data[instance]['EIP']:
                eip = self.data[instance]['EIP'][interface]
                new_eip = EIP()
                new_eip.AccountId = self.account_id
                new_eip.instanceId = instance
                new_eip.MACaddress_orig = eip['']
                new_eip.MACaddress_new =
                new_eip.ifaceId_orig =
                new_eip.ifaceId_new =
                new_eip.privateDNS_orig =
                new_eip.privateDNS_new =
                new_eip.privateIP_orig =
                new_eip.privateIP_new =
                new_eip.publicDNS_orig =
                new_eip.publicDNS_new =
                new_eip.publicIP_orig =
                new_eip.publicIP_new =
                new_eip.SrcDstChk =
                new_eip.SubnetId_orig =
                new_eip.SubnetId_new =
                new_eip.VpcId_orig =
                new_eip.VpcId_new =
"""

