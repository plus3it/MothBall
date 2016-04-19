In order for these tools to connect to the configuration database, it is necessary to provide connection-parameters. These parameters are defined in a file named "mysql.ini". Parameters are defined similar to the following:

~~~ 
[testclt]
user = mothadmin
password = P@ssw0rd
host = 127.0.0.1
database = MothBall
~~~ 

Multiple database connections may be defined within the "mysql.ini" file. Each connection is defined within a "connection-profile".
* Each profile's definition-stanza has a header-block that looks like "[<STRING>]". In the above, this is set via the `[testclt]` line.
* Each profile includes the userid used to connect to the target MySQL database. In the above, this is defined via the `user = mothadmin` line.
* Each profile includes the password used to connect to the target MySQL database. In the above, this is defined via the `password = P@ssw0rd` line.
* Each profile includes the host information for the the target MySQL database. This host information may be given in IP address or hostname (FQDN preferred) form. In the above, this is defined via the `host = 127.0.0.1` line. 
* Each profile includes the name of the target MySQL database. In the above, this is defined via the `database = MothBall` line.
