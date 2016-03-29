#!/bin/python
#
#################################################################
import argparse
import boto3

# Commandline option-handler
parseit = argparse.ArgumentParser()

parseit.add_argument("-r", "--region",
                     choices = ['us-east-1',
                                'us-west-1',
                                'us-west-2'],
                     help="AWS Region",
                     required=True)
parseit.add_argument("-k", "--key",
                     help="AWS access-key ID",
                     required=True)
parseit.add_argument("-s", "--secret",
                     help="AWS access-key secret",
                     required=True)

args = parseit.parse_args()

session = boto3.Session(
    region_name = args.region,
    aws_access_key_id = args.key,
    aws_secret_access_key = args.secret
)

ec2 = session.resource('ec2')

instlist = []
for ret in ec2.instances.all():
    instlist.append(ret._id)
    
print instlist[0:len(instlist)]
