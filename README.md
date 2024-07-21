# AWS Managed Policies Finder

This script helps you **find AWS managed policies that match a given list of allowed permissions**. You just need to write in a **line separated file all the permissions you discovered** you have.

Moreover, this tool checks **up to combinations of 3 different AWS managed policies** that would grant the indicated permissions in the input file.

If you used the tool https://github.com/carlospolop/bf-aws-permissions to discover your permissions you can use the parameter `--check-bf-perms` to **remove false positives** of managed policies combinations that **have all the required permissions, and more that you don't have**.

You can also use the param `--check-with-lacking-perms` to find potential combinations that are missing just 1 or 2 permissions of the ones you have (in case some inline policy is granting them).


## Quick Start

```bash

pip3 install -r requirements.txt

# Help
usage: aws-Perms2ManagedPolicies.py [-h] --permissions-file PERMISSIONS_FILE [--check-bf-perms] [--check-with-lacking-perms]

Find combinations of AWS managed policies that together match a list of allowed permissions.

options:
  -h, --help            show this help message and exit
  --permissions-file PERMISSIONS_FILE
                        Path to the file containing allowed permissions, one per line
  --check-bf-perms      Try to remove false possitives by removed combinations that require you to have other permissions if you have used the tool https://github.com/carlospolop/bf-aws-permissions
  --check-with-lacking-perms
                        Find combinations of managed policies that are lacking one or two permissions


# Check example permissions
python3 aws-Perms2ManagedPolicies.py --permissions-file example-permissions.txt                 

Optimal combinations of AWS managed policies:
- AdministratorAccess
- PowerUserAccess
- ReadOnlyAccess
- AmazonChimeFullAccess
- AmazonChimeReadOnly


# Check example permissions gathered using https://github.com/carlospolop/bf-aws-permissions (remove false positives)
python3 aws-Perms2ManagedPolicies.py --permissions-file example-permissions.txt --check-bf-perms

Optimal combinations of AWS managed policies:
- AmazonChimeReadOnly


# Check example permissions gathered using https://github.com/carlospolop/bf-aws-permissions (remove false positives) and also for combinations lacking some permissions
python3 aws-Perms2ManagedPolicies.py --permissions-file example-permissions.txt --check-with-lacking-perms --check-bf-perms

Optimal combinations of AWS managed policies:
- AmazonChimeReadOnly


# Check example permissions checking also for combinations lacking some permissions
python3 aws-Perms2ManagedPolicies.py --permissions-file example-permissions.txt --check-with-lacking-perms

Optimal combinations of AWS managed policies:
- AdministratorAccess
- PowerUserAccess
- ReadOnlyAccess
- AmazonChimeFullAccess
- AmazonChimeReadOnly

Combinations of AWS managed policies that lack one permission:
- SecurityAudit, AWSSupplyChainFederationAdminAccess, AWSSupportServiceRolePolicy, Lacking chime:GetPhoneNumberSettings
- SecurityAudit, AWSSupportServiceRolePolicy, AWSSupplyChainFederationAdminAccess, Lacking chime:GetPhoneNumberSettings
- AmazonChimeVoiceConnectorServiceLinkedRolePolicy, AWSSupplyChainFederationAdminAccess, AWSSupportServiceRolePolicy, Lacking chime:GetPhoneNumberSettings
- AmazonChimeVoiceConnectorServiceLinkedRolePolicy, AWSSupportServiceRolePolicy, AWSSupplyChainFederationAdminAccess, Lacking chime:GetPhoneNumberSettings
- AWSSupplyChainFederationAdminAccess, AWSSupportServiceRolePolicy, Lacking chime:GetPhoneNumberSettings

Combinations of AWS managed policies that lack two permissions:
- SecurityAudit, AmazonChimeVoiceConnectorServiceLinkedRolePolicy, AWSSupplyChainFederationAdminAccess, Lacking chime:GetPhoneNumberSettings, chime:GetGlobalSettings
- SecurityAudit, AmazonChimeVoiceConnectorServiceLinkedRolePolicy, AWSSupportServiceRolePolicy, Lacking chime:GetMessagingSessionEndpoint, chime:GetPhoneNumberSettings
- SecurityAudit, AWSSupplyChainFederationAdminAccess, AmazonChimeVoiceConnectorServiceLinkedRolePolicy, Lacking chime:GetPhoneNumberSettings, chime:GetGlobalSettings
- SecurityAudit, AWSSupportServiceRolePolicy, Lacking chime:GetMessagingSessionEndpoint, chime:GetPhoneNumberSettings
- AmazonChimeVoiceConnectorServiceLinkedRolePolicy, AWSSupplyChainFederationAdminAccess, Lacking chime:GetPhoneNumberSettings, chime:GetGlobalSettings
- AmazonChimeVoiceConnectorServiceLinkedRolePolicy, AWSSupportServiceRolePolicy, Lacking chime:GetMessagingSessionEndpoint, chime:GetPhoneNumberSettings
```

### Potential false negatives from brute-forcing permissions

- In case you gather your permissions brute-forcing `Get*`, `Describe*` and `List*` permissions and you have indicated the `--check-bf-perms` param. If the principal is allowed to perform an action but **only over an specific condition** and the brute-forcing didn't discover it's allowed to perform that action, the script will not find the managed policy as it it's missing the permission.
  - In order to **reduce these kind of false negatives**, this tool also checks for managed policies combinations that **lacks one or two of the expected permissions**.

- In a similar case, if you found some permissions and some AWS managed policies combinations are lacking just 1 or 2 of those permissions (maybe because they were granted via inline policies) you can use the param `--check-with-lacking-perms` to find potential combinations that are missing just 1 or 2 permissions.
