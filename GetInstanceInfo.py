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
    instArchitecture = inst.architecture
    instBlockDevs = inst.block_device_mappings
    instClientToken = inst.client_token
    instEBSoptimized = inst.ebs_optimized
    instInstanceProfile = inst.iam_instance_profile
    instAMIid = inst.image_id
    instInstanceType = inst.instance_type
    instKeyName = inst.key_name
    instMonitoring = inst.monitoring
    InstMacAddress = inst.network_interfaces_attribute[0]['MacAddress']
    InstEniName = inst.network_interfaces_attribute[0]['NetworkInterfaceId']
    InstEniAttachId = inst.network_interfaces_attribute[0]['Attachment']['AttachmentId']
    instAZ = inst.placement['AvailabilityZone']
    instTenancy = inst.placement['Tenancy']
    instPlaceGrp = inst.placement['GroupName']
    instPrivDnsName = inst.private_dns_name
    instPrivIpAddr = inst.private_ip_address
    instProductCodes = inst.product_codes
    instPubDnsName = inst.public_dns_name
    instPubIpAddr = inst.public_ip_address
    instRootDevName = inst.root_device_name
    instRootVolId = instBlockDevs[0]['Ebs']['VolumeId']
    instSecGroups = inst.security_groups
    instSrcDstChk = inst.source_dest_check
    instSpotReqId = inst.spot_instance_request_id
    instSriovSuppt = inst.sriov_net_support
    instSubnetId = inst.subnet_id			# We also want to grab its name
    instTags = json.dumps(inst.tags)
    instVirtType = inst.virtualization_type
    instVpcId = inst.vpc_id

    insert_map = (
        "INSERT INTO Volume "
        "("
           "AccountId, "
           "instanceId, "
           "amiLaunchIndex, "
           "architecture, "
           "blockDevices_orig, "
           "blockDevices_new, "
           "clientToken, "
           "ebsOptimized, "
           "hypervisor, "
           "iamInstanceProfile, "
           "instanceLifecycle, "
           "instanceType, "
           "kernelId, "
           "keyName, "
           "launchTime, "
           "monitoring, "
           "networkInterfaceSet, "
           "placement, "
           "platform, "
           "privateDnsName_orig, "
           "privateDnsName_new, "
           "privateIpAddress_orig, "
           "privateIpAddress_new, "
           "productCodes, "
           "dnsName_orig, "
           "dnsName_new, "
           "ipAddress_orig, "
           "ipAddress_new, "
           "ramdiskId, "
           "rootDeviceName, "
           "rootDeviceType, "
           "groupSet, "
           "sourceDestCheck, "
           "spotInstanceRequestId, "
           "sriovNetSupport, "
           "instanceState, "
           "stateReason, "
           "reason, "
           "subnetId, "
           "tagSet, "
           "virtualizationType, "
           "vpcId "
        ") VALUES ("
           "%(AccountId)s, "
           "%(instanceId)s, "
           "%(amiLaunchIndex)s, "
           "%(architecture)s, "
           "%(blockDevices_orig)s, "
           "%(blockDevices_new)s, "
           "%(clientToken)s, "
           "%(ebsOptimized)s, "
           "%(hypervisor)s, "
           "%(iamInstanceProfile)s, "
           "%(instanceLifecycle)s, "
           "%(instanceType)s, "
           "%(kernelId)s, "
           "%(keyName)s, "
           "%(launchTime)s, "
           "%(monitoring)s, "
           "%(networkInterfaceSet)s, "
           "%(placement)s, "
           "%(platform)s, "
           "%(privateDnsName_orig)s, "
           "%(privateDnsName_new)s, "
           "%(privateIpAddress_orig)s, "
           "%(privateIpAddress_new)s, "
           "%(productCodes)s, "
           "%(dnsName_orig)s, "
           "%(dnsName_new)s, "
           "%(ipAddress_orig)s, "
           "%(ipAddress_new)s, "
           "%(ramdiskId)s, "
           "%(rootDeviceName)s, "
           "%(rootDeviceType)s, "
           "%(groupSet)s, "
           "%(sourceDestCheck)s, "
           "%(spotInstanceRequestId)s, "
           "%(sriovNetSupport)s, "
           "%(instanceState)s, "
           "%(stateReason)s, "
           "%(reason)s, "
           "%(subnetId)s, "
           "%(tagSet)s, "
           "%(virtualizationType)s, "
           "%(vpcId)s "
        "); "
    )

    insert_data = {
            'AccountId'			: AWSaccount,
            'instanceId'		: instance,
            'amiLaunchIndex'		: '',
            'architecture'		:
            'blockDevices_orig'		: instRootDevName,
            'blockDevices_new'		: '',
            'clientToken'		: instClientToken,
            'ebsOptimized'		: instEBSoptimized,
            'hypervisor'		: 'xen',
            'iamInstanceProfile'	: instInstanceProfile,
            'instanceLifecycle'		: '',
            'instanceType'		: instInstanceType,
            'kernelId'			: '',
            'keyName'			: instKeyName,
            'launchTime'		: '',
            'monitoring'		: instMonitoring,
            'networkInterfaceSet'	: '',
            'placement'			: instAZ,
            'platform'			: '',
            'privateDnsName_orig'	: instPrivDnsName,
            'privateDnsName_new'	: '',
            'privateIpAddress_orig'	: instPrivIpAddr,
            'privateIpAddress_new'	: '',
            'productCodes'		: instProductCodes,
            'dnsName_orig'		: instPubDnsName,
            'dnsName_new'		: '',
            'ipAddress_orig'		: instPubIpAddr,
            'ipAddress_new'		: '',
            'ramdiskId'			: '',
            'rootDeviceName'		: instRootDevName,
            'rootDeviceType'		: 'ebs',
            'groupSet'			: instSecGroups,
            'sourceDestCheck'		: instSrcDstChk,
            'spotInstanceRequestId'	: instSpotReqId,
            'sriovNetSupport'		: instSriovSuppt,
            'instanceState'		: '',
            'stateReason'		: '',
            'reason'			: '',
            'subnetId'			:
            				: instBlockDevs,
            				: instAMIid,
            				: InstMacAddress,
            				: InstEniName,
            				: InstEniAttachId,
            				: instTenancy,
            				: instPlaceGrp,
            				: instRootVolId,
            'subnetId'			: instSubnetId,
            'tagSet'			: instTags,
            'virtualizationType'	: instVirtType,
            'vpcId'			: instVpcId
     }


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

