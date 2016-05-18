import boto3
import logging

class AWSManager(object):

    def __init__(self, region, key, secret):
        self.region = region
        self.key = key
        self.secret = secret
        self.ec2_instances = None
        self.ec2_session = None

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

    def _get_ebs_volume_info(self):
        pass

    def _get_eip_info(self):
        pass




