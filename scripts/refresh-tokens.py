#!/usr/bin/env python

import os
from typing import List, Dict

import wmill
import boto3

# requires WM_TOKEN to be set in the environment to communicate with the
# associated windmill instance

def main(groups: list):
    s = boto3.session.Session(region_name="us-east-2")
    iam_c = s.client('iam')
    sts_c = s.client('sts')
    caller_id = sts_c.get_caller_identity()
    for g in get_wmill_groups():
        variable = f"g/{g}/aws"
        wmill.set_variable(variable, get_token(g))
        print(f"Set token for group {g}")
        print(wmill.get_variable(variable))


def get_likely_iam_groups(prefix: str, session: boto3.session.Session) -> Dict[str, dict]:
    """Role names should be prefixed by the :prefix: argument.
    The IAM role can have the filed names corresponding to the windmill workspace, and a final group.
    Since it's possible for groups and workspaces to have various charcters, the convention will be that
    the workspace is determined by w=<workspace name> and the group by g=<group name>.

    So if the windmill IAM role space starts with is ``windmill-stage`` and we have a workspace called ``infra`` and a group called
    ``aws-ro`` the IAM role that would be matched with that, if it exists, would be called
    ``/windmill-stage/w=infra/g=aws-ro``

    """
    iam_c = session.client('iam')
    marker = None
    all_matching_role_names = list()
    while True:
        if marker:
            result = iam_c.list_roles(PathPrefix=prefix, Marker=marker)
        else:
            result = iam_c.list_roles(PathPrefix=prefix)
        for r in result['Roles']:
            all_matching_role_names.append({r['RoleName']: r['Arn']})

        if result['IsTruncated'] is False:
            break
        marker = result['Marker']



def get_aws_token(group: str, session: boto3.session.Session) -> dict[str, str]:
    return f"token-{group}"


def get_wmill_workspaces() -> list:
    from windmill_api.api.workspaces import list_workspaces_as_super_admin
    return list_workspaces_as_super_admin.sync(client=wmill.create_client(), workspace=wmill.get_workspace())
