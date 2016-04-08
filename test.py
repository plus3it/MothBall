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
      "(AccountId, "
       "instanceId, "
       "amiLaunchIndex, "
       "architecture, "
       "keyName) "
      "VALUES ( "
       "%(AccountId)s, "
       "%(instanceId)s, "
       "%(amiLaunchIndex)s, "
       "%(architecture)s, "
       "%(keyName)s)"
   )

insert_data = {
       'AccountId' : '701759196663',
       'instanceId' : 'i-129af291',
       'amiLaunchIndex' : '0',
       'architecture' : 'x86_64',
       'blockDevices_orig' : '["vol-2b1d7896"]',
       'networkInterfaceSet' : '["eni-963273cc"]',
       'keyName' : 'thjones2-1024b'
   }

cursor.execute(insert_struct, insert_data)
dbconn.commit()

cursor.close()
dbconn.close()
