#!/bin/python
#
#################################################################
import argparse
import boto3
from MyDBconnect import DbConnect, DbCnctInfo

#################################
# Get list of instances in region
def GetInstances():
    ec2 = session.resource('ec2')

    instlist = []
    for ret in ec2.instances.all():
        instlist.append(ret._id)

    return instlist


#############################
# Get Instance's key EBS info
def GetEBSattribs(EBSstruct):
    EBSdict = {}

    for EBS in EBSstruct:
        EBSattach = EBS['DeviceName']
        EBSstruct = EBS['Ebs']
        EBSvol = EBSstruct['VolumeId']

        EBSdict[EBSvol] = EBSattach

    return EBSdict


###################
# Client Attributes
def GetUserData(InstId):
    response = client.describe_instance_attribute(
        InstanceId = InstId,
        Attribute = 'userData'
    )

    UserData = response['UserData']

    if UserData:
        return UserData['Value']
    else:
        return 'None'


############################
# Commandline option-handler
parseit = argparse.ArgumentParser()

parseit.add_argument("-r", "--region",
                     choices = ['us-east-1',
                                'us-west-1',
                                'us-west-2'],
                     help="AWS Region",
                     required=True)
parseit.add_argument("-k", "--key",
                     help="AWS access-key ID")
parseit.add_argument("-s", "--secret",
                     help="AWS access-key secret")

args = parseit.parse_args()

# Initialize session/connection
session = boto3.Session(
    region_name = args.region,
    aws_access_key_id = args.key,
    aws_secret_access_key = args.secret
)

resources = boto3.resource(
    'ec2',
    region_name = args.region,
    aws_access_key_id = args.key,
    aws_secret_access_key = args.secret
)

client = boto3.client(
    'ec2',
    region_name = args.region,
    aws_access_key_id = args.key,
    aws_secret_access_key = args.secret
)
    
# Extract config-info from instances
Instances = GetInstances()
for InstId in Instances:
    # Resource Attributes
    InstInfo = resources.Instance(InstId)
    InstKey = InstInfo.key_name
    InstIAM = InstInfo.iam_instance_profile
    InstType = InstInfo.instance_type
    InstAZ = InstInfo.placement['AvailabilityZone']
    InstPrivDNS = InstInfo.private_dns_name
    InstPrivIP = InstInfo.private_ip_address
    InstPubDNS = InstInfo.public_dns_name
    InstPubIP = InstInfo.public_ip_address
    InstSGlist = InstInfo.security_groups
    InstSubnet = InstInfo.subnet_id
    InstVPC = InstInfo.vpc_id
    InstRootDevName = InstInfo.root_device_name
    InstRootDevType = InstInfo.root_device_type
    InstBlkDevs = GetEBSattribs(InstInfo.block_device_mappings)
    InstAMI = InstInfo.image_id
    InstUserData = GetUserData(InstId)
    
    print InstUserData
    print '=========='


