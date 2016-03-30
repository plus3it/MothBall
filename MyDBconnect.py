#!/bin/python
#
# Simple MySQL connection-test using an externalized
# connection-profile
#
#################################################################
from ConfigParser import SafeConfigParser
import mysql.connector

###########################################
# Pull connect-info from connection-profile
def DbCnctInfo(stanza):
    config = SafeConfigParser()
    config.read('mysql.ini')

    connect_dict = {}
    connect_dict['user'] = config.get(stanza, 'user')
    connect_dict['password'] = config.get(stanza, 'password')
    connect_dict['database'] = config.get(stanza, 'database')
    connect_dict['host'] = config.get(stanza, 'host')

    return connect_dict


############################
# Connect to target MySQL DB
def DbConnect(conn_dict):

    try:
        mconn = mysql.connector.connect(
            user = conn_dict['user'],
            password = conn_dict['password'],
            database = conn_dict['database'],
            host = conn_dict['host']
        )
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print "Successful connect"
        return mconn
