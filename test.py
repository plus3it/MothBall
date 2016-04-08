#!/bin/python
#
#################################################################

import argparse
import boto3
from MyDBconnect import DbConnect, DbCnctInfo

dbconn = DbConnect(DbCnctInfo('testclt'))

cursor = dbconn.cursor()

insert_struct = (
      "Insert INTO Instance "
      "("
        "AccountId, "
        "instanceId, "
        "amiLaunchIndex, "
        "architecture, "
        "blockDevices_orig, "
        "ebsOptimized, "
        "hypervisor, "
        "iamInstanceProfile, "
        "instanceType, "
        "keyName, "
        "privateDnsName_orig, "
        "privateIpAddress_orig, "
        "dnsName_orig, "
        "ipAddress_orig, "
        "rootDeviceName, "
        "rootDeviceType, "
        "groupSet, "
        "sriovNetSupport, "
        "subnetId, "
        "vpcId "
      ") "
      "VALUES ( "
        "%(AccountId)s, "
        "%(instanceId)s, "
        "%(amiLaunchIndex)s, "
        "%(architecture)s, "
        "%(blockDevices_orig)s, "
        "%(ebsOptimized)s, "
        "%(hypervisor)s, "
        "%(iamInstanceProfile)s, "
        "%(instanceType)s, "
        "%(keyName)s, "
        "%(privateDnsName_orig)s, "
        "%(privateIpAddress_orig)s, "
        "%(dnsName_orig)s, "
        "%(ipAddress_orig)s, "
        "%(rootDeviceName)s, "
        "%(rootDeviceType)s, "
        "%(groupSet)s, "
        "%(sriovNetSupport)s, "
        "%(subnetId)s, "
        "%(vpcId)s "
       ") "
   )

insert_data = {
       'AccountId' : '701759196663',
       'instanceId' : 'i-129af291',
       'amiLaunchIndex' : '0',
       'architecture' : 'x86_64',
       'blockDevices_orig' : '["vol-2b1d7896"]',
       'ebsOptimized' : '0',
       'hypervisor' : 'xen',
       'iamInstanceProfile' : 'Instance-BnR',
       'instanceType' : 't2.micro',
       'networkInterfaceSet' : '["eni-963273cc"]',
       'keyName' : 'thjones2-1024b',
       'privateDnsName_orig' : 'ip-172-31-12-197.us-west-1.compute.internal',
       'privateIpAddress_orig' : '172.31.12.197',
       'dnsName_orig' : 'NONE',
       'ipAddress_orig' : 'NONE',
       'rootDeviceName' : '/dev/sda1',
       'rootDeviceType' : 'ebs',
       'groupSet' : '["Remote Access - thjones2", "default"]',
       'sriovNetSupport' : '0',
       'subnetId' : 'subnet-2e714068',
       'vpcId' : 'vpc-3729c952'
   }

cursor.execute(insert_struct, insert_data)
dbconn.commit()

cursor.close()
dbconn.close()
