#!/bin/python
#
# Iterate all the instances within a specific region and turn
# them off.
#
#################################################################
import argparse
import boto3
import subprocess

###################################################################
# Get list of regions in service
#    Need this for bounds-checking, but it's a Chicken/Egg problem:
#    need AWS CLI config with default-region set
def ValidRegion():
    regraw = subprocess.Popen(
            "aws ec2 describe-regions --query 'Regions[].RegionName[]' --out text",
            shell=True,
            stdout=subprocess.PIPE).stdout.read()

    return regraw.split( )

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

###########################
# Get EBS vols for instance
def GetEBSvolInfo(instid):

    ec2 = session.resource('ec2')
    inst = ec2.Instance(id=instid)
    devstruct = inst.block_device_mappings

    devmap = {}
    for dev in devstruct:
        devvolid = dev['Ebs']['VolumeId']
        ebs = {}
        ebs['Mount'] = dev['DeviceName']
        ebs['Size'] = ec2.Volume(devvolid).size
        ebs['Type'] = ec2.Volume(devvolid).volume_type
        ebs['IOPS'] = ec2.Volume(devvolid).iops
        devmap[devvolid] = ebs

    return devmap


############################
# Commandline option-handler
parseit = argparse.ArgumentParser()

parseit.add_argument("-r", "--region",
                     choices = ValidRegion(),
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
    instVols = GetEBSvolInfo(inst)
    print instVols
