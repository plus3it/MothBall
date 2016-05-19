import json
import boto3
import logging


class AWSManager(object):

    def __init__(self, region, key, secret):
        # type: str, str, str

        self.region = region
        self.key = key
        self.secret = secret
        self.ec2_instances = None
        self.ec2_session = None
        self.data = dict()

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

    def get_info(self):

        if not self.ec2_instances:
            self._get_ec2_instances()

        for instance in self.ec2_instances:
            if instance in self.data:
                logging.warning('Instance {0} already exists in Data?'.format(instance))

            self.data[instance] = dict()
            self._get_ebs_volume_info(instance)
            self._get_eip_info(instance)
