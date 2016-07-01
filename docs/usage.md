
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

