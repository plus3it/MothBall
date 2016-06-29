import os
import yaml
import logging
import argparse

from mothball.managers.base import AWSManager

def get_config(filename):
    config = None
    if os.path.exists(filename):
        with open(filename) as f:
            data = f.read()
        config = yaml.load(data)
    else:
        logging.error('config file does not exist!')
    return config

def main(filename):
    config = get_config(filename)
    aws = AWSManager(config['AWS']['region'],
                     config['AWS']['access_key'],
                     config['AWS']['secret_key'],
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
    aws.get_db_connection()
    aws.get_info()




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', dest='filename', default='mothball.config')


    main(parser.parse_args().filename)
