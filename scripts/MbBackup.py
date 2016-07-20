#!/usr/bin/env python

import os
import sys
import yaml
import logging
import argparse

from mothball.managers.base import AWSManager


def get_config(filename):
    """
    Loads Yaml file into a dictionary for use in main.

    :param filename: Path to yaml file for parsing.
    :type filename: basestring

    :return: The data from the yaml config file.
    :rtype: dict
    """

    config = None
    if os.path.exists(filename):
        with open(filename) as f:
            data = f.read()
        config = yaml.load(data)
    else:
        logging.error('config file does not exist!')
    return config


def validate(config):
    # TODO Validation!
    return True


def main(filename, validate, backup, configuration, terminate):
    """
        This is the main caller for the mothball application. This file should be installed and executed on the
    command line.

    This function setups the cadence for backing up and terminating all available ec2 instances for an account.

    Cadence:
        First, it collects the data from the config file.
        Second, it creates an AWSManager which is the core of the mothball interface to aws.
        Third, it collects the account info for the EC2 instance it is being executed on.
        Fourth, it creates the Database connection for dumping data to. Finally it dumps the data to the Database.
        Finally, executes terminate across all instances returned from the get_info function.

    :param filename: This is the mothball.config file for executing the mothball application.
    :type filename: basestring
    :param validate:
    :type validate: bool
    :param backup:
    :type backup: bool
    :param configuration:
    :type configuration: bool
    :param terminate:
    :type termiante: bool
    :return: None
    """

    config = get_config(filename)

    if validate:
        if not validate(config):
            print('Validation has failed!')
            sys.exit()

    aws = AWSManager(config['AWS']['region'],
                     config['AWS']['access_key'],
                     config['AWS']['secret_key'],
                     config['RDS']['region'],
                     config['RDS']['access_key'],
                     config['RDS']['secret_key'],
                     config['Database']['username'],
                     config['Database']['password'],
                     config['Database']['name'],
                     config['Database']['host'],
                     config['Database']['port'],
                     config['Database']['type'],
                     config['RDS']['use_rds'],
                     config['RDS']['name'],
                     *config['RDS']['vpc_security_groups'])

    aws.get_account_info()
    instances = aws.get_instances()

    if configuration:
        try:
            aws.get_db_connection()
            aws.backup_instances()
        except Exception as e:
            print('Configuration has failed.\n{0}'.format(e))
            sys.exit(1)

    if backup:
        try:
            aws.create_snapshots()
        except Exception as e:
            print('Backup has failed.\n{0}'.format(e))
            sys.exit(1)

    if terminate:
        try:
            aws.terminate(instances)
        except Exception as e:
            print('Terminate has failed.\n{0}'.format(e))
            sys.exit(1)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', dest='filename', default='mothball.config',
                        help='This points to the mothball.config file to be used.')
    parser.add_argument('--validate', dest='validate', default=False, action='store_true',
                        help='This option is used to validate your config file.  If using AWS accounts '
                             'it will also validate the keys work. No other options will work when using '
                             'this option other then --config which is necessary')
    parser.add_argument('--backup', dest='backup', default=False, action='store_true',
                        help='This creates snapshots of all of the EBS volumes.')
    parser.add_argument('--configurations', dest='configurations', default=False, action='store_true',
                        help='This updates or creates a database with the configuration data for the account.')
    parser.add_argument('--terminate', dest='terminate', default=False, action='store_true',
                        help='This option must be used in order to turn dryrun off.  In dryrun mode data is stored '
                             'in the database; however will not snapshot the volumes nor terminate the Instance.  When '
                             'this option is used it will turn off dryrun. Be careful this will terminate all ec2 '
                             'instances in a region for the account being used!')

    args = parser.parse_args()

    if not args.filename:
        print('Configuration file must be specified in order to use MbBackup.')
    elif args.validate and any(x for x in [args.backup, args.configurations, args.terminate]):
        print('--validate can only be used by itself and not with another action.')
    elif not any(x for x in [args.backup, args.configurations, args.terminate]):
        print('No action other than --config was specified.  There is nothing to do.')

    main(args.filename, args.validate, args.backup, args.configurations, args.terminate)
