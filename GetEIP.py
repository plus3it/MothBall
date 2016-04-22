#!/bin/python
#
# Iterate all the instances within a specific region and identify
# all attached EIP objects. Record EIP information into the 'EIP'
# (MySQL) database table.
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


# Get EIP info
def GetEipInfo(instance):
    ec2 = session.resource('ec2')
    instStruct = ec2.Instance(id=instance)
    instIface = instStruct.network_interfaces_attribute

##     print instIface
    eipDescription = instIface[0]['Description']
    eipMac = instIface[0]['MacAddress']
    eipNetIfId = instIface[0]['NetworkInterfaceId']
    eipOwnerId = instIface[0]['OwnerId']
    eipOwnerId = instIface[0]['OwnerId']
    eipPrivDns = instIface[0]['PrivateDnsName']
    eipPrivIpAddr = instIface[0]['PrivateIpAddress']
    eipSrcDstChk = instIface[0]['SourceDestCheck']
    eipStat = instIface[0]['Status']
    eipSubnetId = instIface[0]['SubnetId']
    eipVpcId = instIface[0]['VpcId']

    print eipDescription
    print eipMac
    print eipNetIfId
    print eipOwnerId
    print eipOwnerId
    print eipPrivDns
    print eipPrivIpAddr
    print eipSrcDstChk
    print eipStat
    print eipSubnetId
    print eipVpcId

##     eipStruct = ec2.NetworkInterface(id=instance)
##     instArchitecture = inst.architecture
##     instBlockDevs = inst.block_device_mappings
##     instClientToken = inst.client_token
##     instEBSoptimized = inst.ebs_optimized
##     instInstanceProfile = json.dumps(inst.iam_instance_profile)
##     instAMIid = inst.image_id
##     instInstanceType = inst.instance_type
##     instKeyName = inst.key_name
##     instMonitoring = json.dumps(inst.monitoring)
## 
##     if inst.network_interfaces_attribute
##     
##     print eipStruct.association_attribute
##     print eipStruct.attachment
##     print eipStruct.availability_zone
##     print eipStruct.description
##     print eipStruct.groups
##     print eipStruct.interface_type
##     print eipStruct.mac_address
##     print eipStruct.network_interface_id
##     print eipStruct.owner_id
##     print eipStruct.private_dns_name
##     print eipStruct.private_ip_address
##     print eipStruct.private_ip_addresses
##     print eipStruct.requester_id
##     print eipStruct.requester_managed
##     print eipStruct.source_dest_check
##     print eipStruct.status
##     print eipStruct.subnet_id
##     print eipStruct.tag_set
##     print eipStruct.vpc_id


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

# Create list of in-region instances to use for querying EIP info
for inst in GetInstances(args):
    GetEipInfo(inst)

# Clean up connection to MySQL
cursor.close()
dbconn.close()
