import argparse
import boto3
import fnmatch
import sys

from typing import List
from termcolor import colored


def load_permissions_from_file(file_path: str) -> List[str]:
    """Load permissions from a file, one per line."""
    with open(file_path, "r") as file:
        permissions = [line.strip() for line in file.readlines()]
    return permissions

def find_matching_managed_policies(allowed_permissions: List[str], profile_name: str) -> List[str]:
    """Find AWS managed policies that include all the specified allowed permissions."""
    session = boto3.Session(profile_name=profile_name)
    iam_client = session.client("iam")

    paginator = iam_client.get_paginator("list_policies")

    matching_policies = []
    for page in paginator.paginate(Scope="AWS"):
        for policy in page["Policies"]:
            sys.stdout.flush()
            print(f"Checking policy: {policy['PolicyName']}                          \r", end="")
            sys.stdout.flush()

            policy_version = iam_client.get_policy_version(
                PolicyArn=policy["Arn"], VersionId=policy["DefaultVersionId"]
            )
            policy_doc = policy_version["PolicyVersion"]["Document"]

            policy_permissions = []
            not_policy_permissions = []
            
            # Make sure the "Statement" key is a list
            if type(policy_doc["Statement"]) is dict:
                policy_doc["Statement"] = [policy_doc["Statement"]]
            
            for statement in policy_doc["Statement"]:
                if statement["Effect"] == "Allow":
                    if "Action" in statement:
                        policy_permissions.extend(statement["Action"])
                    if "NotAction" in statement:
                        not_policy_permissions.extend(statement["NotAction"])

            # Check if each allowed permission is present in the policy
            permission_match = True
            for perm in allowed_permissions:                
                if not any(fnmatch.fnmatch(perm, policy_perm) for policy_perm in policy_permissions) \
                    and not any(fnmatch.fnmatch(perm, not_policy_perm) for not_policy_perm in not_policy_permissions):
                    permission_match = False
                    break

            if permission_match:
                matching_policies.append(policy["PolicyName"])

    return matching_policies


def main(aws_profile: str, permissions_file: str):
    allowed_permissions = load_permissions_from_file(permissions_file)
    matching_policies = find_matching_managed_policies(allowed_permissions, aws_profile)

    print("")
    print(colored("Matching AWS managed policies:", "green"))
    for policy in matching_policies:
        print(colored(f"- {policy}", "yellow"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find AWS managed policies matching a list of allowed permissions.")
    parser.add_argument("--profile", type=str, required=True, help="AWS profile name to use")
    parser.add_argument("--permissions-file", type=str, required=True, help="Path to the file containing allowed permissions, one per line")

    args = parser.parse_args()
    main(aws_profile=args.profile, permissions_file=args.permissions_file)