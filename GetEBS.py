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

    # Define INSERT-string to pass to MySQL
    # and associated value-mapping 
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
	  "%(AccountId)s, "
          "%(instanceId)s, "
          "%(attachmentSet)s, "
          "%(availabilityZone)s, "
          "%(encrypted)s, "
          "%(iops)s, "
          "%(kmsKeyId)s, "
          "%(size)s, "
          "%(snapshotId)s, "
          "%(status)s, "
          "%(tagSet)s, "
          "%(volumeId)s, "
          "%(volumeType)s"
	"); "
    )

    # Extract values from passed-EBS structure
    instance = insertData.keys()[0]
    for volume in insertData[instance]:
        volMount = insertData[instance][volume]['Mount']
        volIops = insertData[instance][volume]['IOPS']
        if volIops is None:
            volIops = 0
        volType = insertData[instance][volume]['Type']
        volSize = insertData[instance][volume]['Size']

        # Define mappings to SQL-managed values
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

        # Insert row into Volume table
        print('Writing volume \'%s\' for instance \'%s\' to Volume table' % (volume, instance))
        cursor.execute(insert_struct, insert_data)
        dbconn.commit()


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

# Initialize session/connection to AWS
session = boto3.Session(
    region_name = args.region,
    aws_access_key_id = args.key,
    aws_secret_access_key = args.secret
)

# Initialize connection to MySQL
dbconn = DbConnect(DbCnctInfo('testclt'))
cursor = dbconn.cursor()

# Create list of in-region instances to stop
for inst in GetInstances(args):
    instVols = GetEBSvolInfo(inst)
    # print instVols
    ebsMysql(instVols)


# Clean up connection to MySQL
cursor.close()
dbconn.close()
