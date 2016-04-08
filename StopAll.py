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

# Initiate EC2 connection
ec2 = boto3.resource(
    'ec2',
    region_name = args.region,
    aws_access_key_id = args.key,
    aws_secret_access_key = args.secret
)

# Create list of in-region instances to stop
stopList = GetInstances(args)

# Let operator know what we're doing
print "Attempting to stop the following instances:"
for instId in stopList:
    print '  - ' + instId

# Send stop signal to instance-list
ec2.instances.filter(InstanceIds=stopList).stop()
