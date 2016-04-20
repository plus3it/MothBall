#!/bin/python
#
# Iterate all the instances within a specific region and capture
# key data to 'Instance' (MySQL) database table.
#
#################################################################
import argparse
import boto3
import json
import subprocess
from MothDBconnect import DbConnect, DbCnctInfo

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


# Get instance info 
def GetInstancInfo(instance):
    ec2 = session.resource('ec2')
    inst = ec2.Instance(id=instance)
    instLaunchIndex = inst.ami_launch_index
    instArchitecture = inst.architecture
    instBlockDevs = inst.block_device_mappings
    instClientToken = inst.client_token
    instEBSoptimized = inst.ebs_optimized
    instHypervisor = inst.hypervisor
    instInstanceProfile = inst.iam_instance_profile
    instAMIid = inst.image_id
    instInstanceId = inst.instance_id
    instInstanceLifecycle = inst.instance_lifecycle
    instInstanceType = inst.instance_type
    instKernelId = inst.kernel_id
    instKeyName = inst.key_name
    instLaunchTime = inst.launch_time
    instMonitoring = inst.monitoring
    instNetIfAttribs = inst.network_interfaces_attribute
    instPlacement = inst.placement
    instPlatform = inst.platform
    instPrivDnsName = inst.private_dns_name
    instPrivIpAddr = inst.private_ip_address
    instProductCodes = inst.product_codes
    instPubDnsName = inst.public_dns_name
    instPubIpAddr = inst.public_ip_address
    instRamdiskId = inst.ramdisk_id
    instRootDevName = inst.root_device_name
    instRootDevType = inst.root_device_type
    instSecGroups = inst.security_groups
    instSrcDstChk = inst.source_dest_check
    instSpotReqId = inst.spot_instance_request_id
    instSriovSuppt = inst.sriov_net_support
    instState = inst.state
    instStateReason = inst.state_reason
    instStateTransReas = inst.state_transition_reason
    instSubnetId = inst.subnet_id
    instTags = inst.tags
    instVirtType = inst.virtualization_type
    instVpcId = inst.vpc_id

    print instLaunchIndex
    print instArchitecture
    print instBlockDevs
    print instClientToken
    print instEBSoptimized
    print instHypervisor
    print instInstanceProfile
    print instAMIid
    print instInstanceId
    print instInstanceLifecycle
    print instInstanceType
    print instKernelId
    print instKeyName
    print instLaunchTime
    print instMonitoring
    print instNetIfAttribs
    print instPlacement
    print instPlatform
    print instPrivDnsName
    print instPrivIpAddr
    print instProductCodes
    print instPubDnsName
    print instPubIpAddr
    print instRamdiskId
    print instRootDevName
    print instRootDevType
    print instSecGroups
    print instSrcDstChk
    print instSpotReqId
    print instSriovSuppt
    print instState
    print instStateReason
    print instStateTransReas
    print instSubnetId
    print instTags
    print instVirtType
    print instVpcId


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
parseit.add_argument("-t", "--target-account",
                     help="AWS account to manage",
                     required=True)

# Assign CLI argument-values to fetchable name-space
args = parseit.parse_args()

AWSaccount = args.target_account

# Initialize session/connection to AWS
session = boto3.Session(
    region_name = args.region,
    aws_access_key_id = args.key,
    aws_secret_access_key = args.secret
)

# Initialize connection to MySQL
dbconn = DbConnect(DbCnctInfo('testclt'))
cursor = dbconn.cursor()

for instance in GetInstances(args):
    GetInstancInfo(instance)

# Clean up connection to MySQL
cursor.close()
dbconn.close()

