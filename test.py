#!/bin/python
#
#################################################################

import argparse
import boto3
from MyDBconnect import DbConnect, DbCnctInfo

dbconn = DbConnect(DbCnctInfo('prototype'))

cursor = dbconn.cursor()

insert_struct = ("Insert INTO InstanceInfo "
                 "(InstanceID, KeyName) "
                 "VALUES (%(instid)s, %(keyid)s)")
insert_data = {
       'instid' : 'i-129af291',
       'keyid' : 'thjones2-1024b'
   }

cursor.execute(insert_struct, insert_data)
dbconn.commit()

cursor.close()
dbconn.close()
