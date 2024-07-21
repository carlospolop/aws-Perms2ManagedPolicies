# AWS Managed Policies Finder

This script helps you **find AWS managed policies that match a given list of allowed permissions**. It takes the AWS profile name and the path to the file containing the list of allowed permissions as input.

For this, you just need to write in a **line separated file all the permissions you discovered** you have.

Moreover, if you used the tool https://github.com/carlospolop/bf-aws-permissions to discover your permissions you can use the parameter `--check-bf-perms` to **remove false positives** of managed policies combinations that **have all the required permissions, and more that you don't have**.


## Quick Start

```bash

pip3 install -r requirements

# Help
usage: aws-Perms2ManagedPolicies.py [-h] --permissions-file PERMISSIONS_FILE [--check-bf-perms]

Find combinations of AWS managed policies that together match a list of allowed permissions.

options:
  -h, --help            show this help message and exit
  --permissions-file PERMISSIONS_FILE
                        Path to the file containing allowed permissions, one per line
  --check-bf-perms      Try to remove false possitives by removed combinations that require you to have other permissions if you have used the tool https://github.com/carlospolop/bf-aws-permissions


# Run example with my profile
python3 aws-Perms2ManagedPolicies.py --permissions-file example-permissions.txt

Optimal combinations of AWS managed policies:
- arn:aws:iam::aws:policy/AdministratorAccess
- arn:aws:iam::aws:policy/PowerUserAccess
- arn:aws:iam::aws:policy/ReadOnlyAccess
- arn:aws:iam::aws:policy/AmazonChimeFullAccess
- arn:aws:iam::aws:policy/AmazonChimeReadOnly

# Run example with my profile and check bf permissions (remove false positives)
python3 aws-Perms2ManagedPolicies.py --permissions-file example-permissions.txt --check-bf-perms

Optimal combinations of AWS managed policies:
- arn:aws:iam::aws:policy/AmazonChimeReadOnly
```
