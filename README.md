[![license](https://img.shields.io/github/license/plus3it/mothball.svg)](./LICENSE)
[![Build Status](https://travis-ci.org/plus3it/mothball.svg)](https://travis-ci.org/plus3it/mothball)

# Mothball
Mothball is a Python package and application for Backing up all ec2 instance configurations for an AWS Account. The
package also snapshot's EBS volumes and terminates instances. Mothball requires that the User executing the script has 
sufficent privledges to collect information about and execute snapshots and termination requests against instances in
their AWS account and region.

## Installation

For installation with Git from source.

```
git clone https://github.com/plus3it/mothball.git
cd mothball
python setup.py build
sudo python setup.py install
```

or for installation with pip

```
sudo pip install mothball
```

Validate that installation was successful and that the cli tool is available

```
MbBackup --help
```

## Configuration

Mothball requires a configuration file.  This file contains the database type and location, authentication information,
and other necessary information for creating or using an RDS database instance.  The configuration


### Configurations for the Database to use.

1 Database:
  # Supported Database types are MySQL and PostgreSQL
  type: mysql

  name: AWSBackup

  username: mothball

  password: mothballP4ssw0rd

  # Host/Port only need to be defined if you are not using RDS and would rather back up to on an on prem or nonRDS db
  host:
  port: 3389

# AWS account information so that Mothball can access the api
AWS:
  region: us-east-1

  access_key: XXXXXXXXXXXXXXXXXXXX

  secret_key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# For use with RDS (either existing or to create one)
RDS:
  use_rds: True
  # Comma seperated for more than one security group.
  vpc_security_groups:

  name:

## Usage

```
python MbBackup.py --help
usage: MbBackup.py [-h] [--config FILENAME] [--terminate]

optional arguments:
  -h, --help         show this help message and exit
  --config FILENAME  This points to the mothball.config file to be used.
  --terminate        This option must be used in order to turn dryrun off. In
                     dryrun mode data is storedin the database; however will
                     not snapshot the volumes nor terminate the Instance.
                     Whenthis option is used it will turn off dryrun. Be
                     careful this will terminate all ec2instances in a region
                     for the account being used!

```



## Documentation
For information on installing and using Mothball, go to https://mothball.readthedocs.io.

Alternatively, you can install mkdocs with
 ```
 pip install mkdocs
 ```
 and then in the Mothball directory, run
 ```
 mkdocs serve
 ```
 This will start a light-weight server on `http://127.0.0.1:8000` containing the documentation on Mothball.
