from mothball.db.models.base import Base, EBS, EIP
from mothball.db.mysql.base import SQLConnect
import time
import json
import boto3
import logging


class AWSManager(object):

    def __init__(self, region, key, secret, username, password, db_type, *vpc_sg):
        # type: str, str, str

        self.region = region
        self.key = key
        self.secret = secret
        self.username = username
        self.password = password
        self.db_type = db_type
        self.ec2_instances = None
        self.ec2_session = None
        self.data = dict()
        self.rds_session = None
        self.vpc_sg = vpc_sg

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

    def _get_ebs_volume_info(self, instance):

        device_structure = self.ec2_session.Instance(instance).block_device_mappings

        if 'EBS' in self.data[instance]:
            logging.warning('EBS Data already exists in instance {0}'.format(instance))
        else:
            self.data[instance]['EBS'] = dict()

        for dev in device_structure:
            device = dict()
            devvolid = dev['Ebs']['VolumeId']
            device['Mount'] = dev['DeviceName']
            device['Size'] = self.ec2_session.Volume(devvolid).size
            device['Type'] = self.ec2_session.Volume(devvolid).volume_type
            device['IOPS'] = self.ec2_session.Volume(devvolid).iops
            device['AZ'] = self.ec2_session.Volume(devvolid).availability_zone
            device['Tags'] = json.dumps(self.ec2_session.Volume(devvolid).tags)

            self.data[instance]['EBS'][devvolid] = device

    def _get_eip_info(self, instance):

        interfaces = self.ec2_session.Instance(instance).network_interfaces_attribute

        if 'EIP' in self.data[instance]:
            logging.warning('EIP Data already exists in instance {0}'.format(instance))
        else:
            self.data[instance]['EIP'] = dict()

        for interface in interfaces:
            nid = interface['NetworkInterfaceId']
            self.data[instance]['EIP'][nid] = dict()
            self.data[instance]['EIP'][nid]['description'] = interface.get('Description')
            self.data[instance]['EIP'][nid]['macAddress'] = interface.get('MacAddress')
            self.data[instance]['EIP'][nid]['interfaceId'] = interface.get('NetworkInterfaceId')
            self.data[instance]['EIP'][nid]['accountId'] = interface.get('OwnerId')
            self.data[instance]['EIP'][nid]['privateDns'] = interface.get('PrivateDnsName')
            self.data[instance]['EIP'][nid]['privateIpAddr'] = interface.get('PrivateIpAddress')
            self.data[instance]['EIP'][nid]['SrcDstChk'] = interface.get('SourceDestCheck')
            self.data[instance]['EIP'][nid]['Status'] = interface.get('Status')
            self.data[instance]['EIP'][nid]['SubnetId'] = interface.get('SubnetId')
            self.data[instance]['EIP'][nid]['VpcId'] = interface.get('VpcId')
            if 'Association' in interface:
                self.data[instance]['EIP'][nid]['publicDns'] = interface['Association'].get('PublicDnsName')
                self.data[instance]['EIP'][nid]['publicIpAddr'] = interface['Association'].get('PublicIp')

    def _check_rds_instance_exists(self, name):
        return any(k for k in self.rds_session.describe_db_instances()['DBInstances'] if k['DBInstanceIdentifier'] == name)

    def _get_rds_db_info(self, name):
        for instance in self.rds_session.describe_db_instances()['DBInstances']:
            if instance['DBInstanceIdentifier'] == name.lower():
                self.instance_info = instance

    def _create_rds_instance(self, name):

        self.rds_session = self.Session.client('rds')

        if not self._check_rds_instance_exists(name):
            self.rds_session.create_db_instance(DBInstanceIdentifier=name,
                                                AllocatedStorage = 200,
                                                DBInstanceClass='db.t2.micro',
                                                DBName='Backup',
                                                Engine=self.db_type,
                                                MasterUsername=self.username,
                                                MasterUserPassword=self.password,
                                                VpcSecurityGroupIds=self.vpc_sg
                                                )

        self._get_rds_db_info(name)
        while 'Endpoint' not in self.instance_info:
            time.sleep(5)
            self._get_rds_db_info(name)


    def _create_rds_tables(self):

        s = SQLConnect(self.instance_info['Endpoint']['Address'],
                       self.instance_info['Endpoint']['Port'],
                       self.username,
                       self.password,
                       self.db_type,
                       )

        s.create_tables()

    def dump_ebs_record(self, ):
        pass

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

