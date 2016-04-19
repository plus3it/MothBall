#!/bin/python
#
# Iterate all the instances within a specific region and turn
# them off.
#
#################################################################
import argparse
import boto3
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

    return { instid : devmap }


#################################
# Insert EBS volume-info into SQL
def ebsMysql(insertData):
    # dbconn = DbConnect(DbCnctInfo('testclt'))
    # cursor = dbconn.cursor()

    insert_struct = (
        "INSERT INTO Volume "
	"("
	  "AccountId, "
          "instanceId, "
          "attachmentSet, "
          "availabilityZone, "
          "encrypted, "
          "iops, "
          "kmsKeyId, "
          "size, "
          "snapshotId, "
          "status, "
          "tagSet, "
          "volumeId, "
          "volumeType"
	") "
	"VALUES ("
	  "'%(AccountId)s', "
          "'%(instanceId)s', "
          "'%(attachmentSet)s', "
          "'%(availabilityZone)s', "
          "'%(encrypted)s', "
          "'%(iops)s', "
          "'%(kmsKeyId)s', "
          "'%(size)s', "
          "'%(snapshotId)s', "
          "'%(status)s', "
          "'%(tagSet)s', "
          "'%(volumeId)s', "
          "'%(volumeType)s'"
	"); "
    )

    instance = insertData.keys()[0]
    for volume in insertData[instance]:
        volMount = insertData[instance][volume]['Mount']
        volIops = insertData[instance][volume]['IOPS']
        if volIops is None:
            volIops = 0
        volType = insertData[instance][volume]['Type']
        volSize = insertData[instance][volume]['Size']

        insert_data = {
	        'AccountId'		: 'TEST',
                'instanceId'		: instance,
                'attachmentSet'		: volMount,
                'availabilityZone'	: 'TEST',
                'createTime'		: '',
                'encrypted'		: '0',
                'iops'			: volIops,
                'kmsKeyId'		: '',
                'size'			: volSize,
                'snapshotId'		: '',
                'status'		: '',
                'tagSet'		: '["NO DATA"]',
                'volumeId'		: volume,
                'volumeType'		: volType
	    }

        print (insert_struct % insert_data)
        # cursor.execute(insert_struct, insert_data)
        # dbconn.commit()
        # cursor.close()

# dbconn.close()



    # print("%s\t%s\t%s\t%s\t%s\t%s" % (instance, volume, volMount, volSize, volType, volIops))
    # Above extraction-loop yields:
    #   instanceId	volumeId	attachmentSet	size	volumeType	iops
    #   i-7f30e7ca      vol-2b1d7896    /dev/sda1       8       gp2     	24
    #   i-7f30e7ca      vol-0594d0b8    /dev/sdf        1       gp2     	3
    #   i-7f30e7ca      vol-1694d0ab    /dev/sdg        1       gp2     	3
    #   i-51077091      vol-3e86d5db    /dev/sda1       20      standard        None


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
    # print instVols
    ebsMysql(instVols)
