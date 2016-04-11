#!/bin/python
#
# Iterate all the instances within a specific region and turn
# them off.
#
#################################################################
import argparse
import boto3

#################################
# Get list of instances in region
def GetInstances(args):

    ec2 = session.resource(
        'ec2',
        region_name = args.region,
        aws_access_key_id = args.key,
        aws_secret_access_key = args.secret
    )

    instlist = []
    for ret in ec2.instances.all():
        instlist.append(ret._id)

    return instlist

# Get EBS vols for instance
def GetEBSvolInfo(instid):

    ec2 = session.resource('ec2')
    inst = ec2.Instance(id=instid)
    devstruct = inst.block_device_mappings
    for dev in devstruct:
        devmount = dev['DeviceName']
        devvolid = dev['Ebs']['VolumeId']


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

# Create list of in-region instances to stop
for inst in GetInstances(args):
    GetEBSvolInfo(inst)
