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