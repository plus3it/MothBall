#!/bin/python
#
#################################################################
import argparse
import boto3

# Get list of instances in region
def GetInstances():
    ec2 = session.resource('ec2')

    instlist = []
    for ret in ec2.instances.all():
        instlist.append(ret._id)

    return instlist

# Get key instance-attributes
def GetInstanceAttribs():
    return

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
    
Instances = GetInstances()
for InstId in Instances:
    InstInfo = resources.Instance(InstId)
    InstKey = InstInfo.key_name
    InstIAM = InstInfo.iam_instance_profile
    InstType = InstInfo.instance_type
    InstAZ = InstInfo.placement['AvailabilityZone']
    InstPrivDNS = InstInfo.private_dns_name
    InstPrivIP = InstInfo.private_ip_address
    InstPubDNS = InstInfo.public_dns_name
    InstPubIP = InstInfo.public_ip_address
    InstRootDevName = InstInfo.root_device_name
    InstRootDevType = InstInfo.root_device_type
    InstSGlist = InstInfo.security_groups
    InstSubnet = InstInfo.subnet_id
    InstVPC = InstInfo.vpc_id
    InstBlkDevs = InstInfo.block_device_mappings

    print InstInfo
    print '=========='
