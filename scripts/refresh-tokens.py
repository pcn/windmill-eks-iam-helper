#!/usr/bin/env python

import json
import os
import time
import datetime
from typing import List, Dict

import wmill
import boto3

from windmill_api.api.workspace import list_workspaces_as_super_admin

from windmill_api.api.folder import list_folders, get_folder, create_folder, update_folder
from windmill_api.models.create_folder_json_body import CreateFolderJsonBody

from windmill_api.api.resource import update_resource, get_resource, create_resource, create_resource_type, exists_resource
from windmill_api.models.update_resource_json_body import UpdateResourceJsonBody
from windmill_api.models.create_resource_json_body import CreateResourceJsonBody
from windmill_api.models.create_resource_type_json_body import CreateResourceTypeJsonBody


# Let's use "iam_creds" as the schema type name
RES_FOLDER = "aws_iam"
RES_TYPE = "iam_creds"
RES_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "properties": {
        "role_name": {
            "type": "string",
            "description": "name of the IAM role",
        },
        "AccessKeyId": {
            "type": "string",
            "description": "the ephermeral AWS access key ID",
        },
        "SecretAccessKey": {
            "type": "string",
            "description": "The ephemeral AWS secret access key",
        },
        "SessionToken": {
            "type": "string",
            "description": "The ephemeral session token for the role credentials",
        },
        "Expiration": {
            "type": "string",
            "description": "The string representation of the time these credentials expire",
        },
        "type": "object",
        "required": ["role_name", "AccessKeyId", "SecretAccessKey", "SessionToken", "Expiration"],
    }
}



# requires
# - BASE_INTERNAL_URL to be the URL (http/https) to communicate
#   with windmill. I think it will always be http://windmill-app in the same namespace.
#   the wmill client uses this directly
# - WM_TOKEN to be set in the environment to authenciate with the
#   associated windmill instance
# - WM_IAM_PATH_PREFIX must be set in the environment to specify the
#   windmill roles' IAM path, e.g. '/windmill-stage/'

def main():
    s = boto3.session.Session(region_name="us-east-2")
    caller_id = s.client('sts').get_caller_identity()

    os.environ["BASE_INTERNAL_URL"] = os.getenv("BASE_INTERNAL_URL", "http://windmill-app:8000")
    print(f"Started with BASE_INTERNAL_URL as  {os.getenv('BASE_INTERNAL_URL')}")
    print(f"Started with caller_identity of {caller_id}")
    print(f"Started with WM_IAM_PATH_PREFIX {os.getenv('WM_IAM_PATH_PREFIX')}")
    while True:
        nowutc = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print(f"logging  {nowutc}")
        ws_names = get_wmill_workspace_names()
        iam_roles = get_likely_iam_roles(os.getenv("WM_IAM_PATH_PREFIX"), s)
        for ws_name_from_iam in iam_roles.keys():
            if ws_name_from_iam in ws_names:
                creds = get_wspace_creds(iam_roles[ws_name_from_iam], s)
                set_ws_folder(ws_name_from_iam, creds)
        sleep_seconds = int(os.getenv("WM_IAM_REFRESH_MINUTES", 5)) * 60
        print(f"Going to sleep for {sleep_seconds} seconds")
        time.sleep(sleep_seconds)


def get_wspace_creds(roles: dict, s):
    """Given a dictionary that looks like this for e.g.  wspace_name='infra',
    roles={'ec2_ro': 'arn:aws:iam::895030038186:role/windmill-cmh-stag/w=infra/ec2_ro', [etc.]}
    return a dictionary of role name and credentials, e.g.
    """
    sts = s.client('sts')
    results = dict()
    for rname, arn in roles.items():
        results[rname] = sts.assume_role(RoleArn=arn, RoleSessionName=f"windmill-{rname}")
    return results


def get_likely_iam_roles(prefix: str, session: boto3.session.Session) -> Dict[str, dict]:
    """Role names should be prefixed by the :prefix: argument.
    The IAM role can have the filed names corresponding to the windmill workspace, and a final group.
    Since it's possible for groups and workspaces to have various charcters, the convention will be that
    the workspace is determined by w=<workspace name> and the group by g=<group name>.

    So if the windmill IAM role space starts with is ``windmill-stage`` and we have a workspace called ``infra`` and a group called
    ``aws-ro`` the IAM role that would be matched with that, if it exists, would be called
    ``ec2-ro``
    and it would be in the namespace:
    ``/windmill-stage/w=infra/``

    """
    iam_c = session.client('iam')
    marker = None
    workspace_roles = dict()
    while True:
        if marker:
            result = iam_c.list_roles(PathPrefix=prefix, Marker=marker)
        else:
            result = iam_c.list_roles(PathPrefix=prefix)
        for r in result['Roles']:
            pth = r['Path']
            wspace = pth.split('/')[2][2:]  # turn /foo/w=<something>/ into <something>
            if not workspace_roles.get(wspace):
                workspace_roles[wspace] = dict()
            workspace_roles[wspace][r['RoleName']] = r['Arn']

        if result['IsTruncated'] is False:
            break
        marker = result['Marker']
    return workspace_roles


def set_ws_folder(ws_name: str, temp_creds: dict):
    folders = _list_folders(ws_name)
    print(f"Temp creds are {temp_creds}")
    if RES_FOLDER not in [f.name for f in folders]:
        _create_folder(ws_name)
    _update_folder(ws_name, temp_creds)


def get_wmill_workspace_names() -> set:
    """Provide a set of workspace names that really exist"""
    workspace_names = set()
    try:
        for wspace in list_workspaces_as_super_admin.sync(client=wmill.create_client()):
            workspace_names.add(wspace.id)
    except TypeError as te:
        print(f"No workspaces discovered: {te} (did you fail to connect to the service?)")
    return workspace_names


def _list_folders(workspace):
    """List the folders that exist in the requested workspace"""
    res = list_folders.sync(workspace=workspace, client=wmill.create_client())
    return res


def create_folder_resource_type(workspace: str):
    """Create a new resource's schema in a workspace to contain IAM permissions"""
    global RES_SCHEMA
    global RES_TYPE
    json_body = CreateResourceTypeJsonBody(
        name=RES_TYPE,
        workspace_id=workspace,
        schema=json.dumps(RES_SCHEMA), description="AWS IAM credentials to assume roles available to users in this workspace")
    create_resource_type.sync_detailed(workspace, json_body=body, client=wmill.create_client())


def _get_folder_resource(workspace: str, path: str):
    result = get_resource.sync(workspace=workspace, path=path, client=wmill.create_client())
    return result


def _update_folder_resource(workspace: str, content: dict):
    """Updates a resource in the workspace/secret. content should be a
    dictionary, that match the schema in RES_SCHEMA to create
    assumable IAM roles
    """
    global RES_TYPE
    global RES_FOLDER

    description = f"Temporary IAM role credentials granted to users of the {workspace} workspace."
    for role_name, vals in content.items():
        path = f"f/{RES_FOLDER}/{role_name}"
        value = {
            "role_name": role_name,
            "AccessKeyId": vals["Credentials"]["AccessKeyId"],
            "SecretAccessKey": vals["Credentials"]["SecretAccessKey"],
            "SessionToken": vals["Credentials"]["SessionToken"],
            "Expiration": vals["Credentials"]["Expiration"],
        }
        print(value)
        if not _get_folder_resource(workspace, path):  # XXX make sure type exists first
            request = CreateResourceJsonBody(path=path, resource_type=RES_TYPE, value=json.dumps(value, default=str), description=description)
            result = create_resource.sync_detailed(workspace, json_body=request, client=wmill.create_client())
        else:
            request = UpdateResourceJsonBody(path=path, value=json.dumps(value, default=str), description=description)
            result = update_resource.sync_detailed(
                workspace=workspace, path=path, json_body=request, client=wmill.create_client())
    print(f"update result is {result} for path {path}")


def _create_folder(workspace: str, folder=RES_FOLDER):
    """If it's not there, create it"""
    request = CreateFolderJsonBody(name=folder)
    result = create_folder.sync_detailed(workspace=workspace, json_body=request, client=wmill.create_client())
    print(f"create result is {result}")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Exception bubbled up to the top: {str(e)}")
        time.sleep(int(os.getenv("WM_IAM_EXCEPT_TIMEOUT_SEC", 5)))
        raise
