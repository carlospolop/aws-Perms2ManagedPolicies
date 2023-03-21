# AWS Managed Policies Finder

This script helps you **find AWS managed policies that match a given list of allowed permissions**. It takes the AWS profile name and the path to the file containing the list of allowed permissions as input.

For this, you just need to use a **profile of your own account** with permission to read all the AWS managed roles.

It takes around **10min** to run this.

## Quick Start

```bash

pip3 install -r requirements

# Help
python3 aws-Perms2ManagedRoles.py -h
usage: aws-Perms2ManagedRoles.py [-h] --profile PROFILE --permissions-file
                         PERMISSIONS_FILE

Find AWS managed policies matching a list of allowed permissions.

optional arguments:
  -h, --help            show this help message and exit
  --profile PROFILE     AWS profile name to use
  --permissions-file PERMISSIONS_FILE
                        Path to the file containing allowed permissions, one
                        per line

# Replace `<aws-profile>` with your AWS profile name and `<permissions-file-path>` with the path to the file containing the allowed permissions.

# Run example with my profile
python3 aws-Perms2ManagedRoles.py --profile myadmin --permissions-file example-permissions.txt
```