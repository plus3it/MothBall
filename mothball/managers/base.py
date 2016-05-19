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

        instIfaces = self.ec2_session.Instance(instance).network_interfaces_attribute

        if 'EIP' in self.data[instance]:
            logging.warning('EIP Data already exists in instance {0}'.format(instance))
        else:
            self.data[instance]['EIP'] = dict()

        for interface in instIfaces:
            eipNetIfId = interface['NetworkInterfaceId']
            self.data[instance]['EIP'][eipNetIfId] = dict()
            self.data[instance]['EIP'][eipNetIfId]['description'] = interface['Description']
            self.data[instance]['EIP'][eipNetIfId]['macAddress'] = interface['MacAddress']
            self.data[instance]['EIP'][eipNetIfId]['interfaceId'] = interface['NetworkInterfaceId']
            self.data[instance]['EIP'][eipNetIfId]['accountId'] = interface['OwnerId']
            self.data[instance]['EIP'][eipNetIfId]['privateDns'] = interface['PrivateDnsName']
            self.data[instance]['EIP'][eipNetIfId]['privateIpAddr'] = interface['PrivateIpAddress']
            self.data[instance]['EIP'][eipNetIfId]['SrcDstChk'] = interface['SourceDestCheck']
            self.data[instance]['EIP'][eipNetIfId]['Status'] = interface['Status']
            self.data[instance]['EIP'][eipNetIfId]['SubnetId'] = interface['SubnetId']
            self.data[instance]['EIP'][eipNetIfId]['VpcId'] = interface['VpcId']
            if 'Association' in interface:
                self.data[instance]['EIP'][eipNetIfId]['publicDns'] = interface['Association'].get('PublicDnsName')
                self.data[instance]['EIP'][eipNetIfId]['publicIpAddr'] = interface['Association'].get('PublicIp')

    def get_info(self):

        if not self.ec2_instances:
            self._get_ec2_instances()

        for instance in self.ec2_instances:
            if instance in self.data:
                logging.warning('Instance {0} already exists in Data?'.format(instance))

            self.data[instance] = dict()
            self._get_ebs_volume_info(instance)
            self._get_eip_info(instance)

