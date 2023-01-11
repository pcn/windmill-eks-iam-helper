# windmill-eks-iam-helper
Help to get windmill credentials from IAM into separate windmill folders for different projects.

# Requirements

- Windmill running in EKS via helm
- windmill account configured to assume a role (for example, the role is `windmill-stage` in this document)
- role assumption configured in AWS IAM to permit the windmill-stage role to assume other roles that are created within the path `/windmill-stage/` (configurable)
- Environment var `"WM_TOKEN"` contains a windmill superadmin token to access the windmill API to create and update required variables across all workspaces 
- Environment var `"WM_IAM_PREFIX"` containing the path in IAM that prefixes our roles, `/windmill-stage/` in this example


# Overview
The idea here is that when running windmill in EKS, that instead of
providing explicit keys, you want to authorization via role assumption. This role assumption can be enabled
as far as the service account for windmill getting a role via IRSA, however the workspaces in windmill cannot do that.


# Implementation
To provide more granularity within windmill, we can create a scheme with IAM namespaces that this helper users to 
place and refresh credentials within the windmill folder of a project which grants all of the users of a project
the ability to use the role assumptions that are provided. 

So provided a terraform situation like this:

```hcl
data "aws_iam_policy_document" "allow_subroles" {
  statement {
    sid = "AllowSubRole1"
    actions = [
      "sts:AssumeRole",
      "iam:ListRoles",
      "iam:GetRole"
    ]
    effect = "Allow"
    resources = ["arn:aws:iam::00000000000:role/windmill-stage/*"]
  }
}

resource "aws_iam_policy" "allow_subroles" {
  name = "wmill_subrole_assumption"
  description = "Allow windmill to assume subroles"
  policy = data.aws_iam_policy_document.allow_subroles.json
}


data "aws_iam_policy_document" "wmill_sub_arp" {
  statement {
    sid = "PcnTestWmill1"
    actions = ["sts:AssumeRole"]
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = ["arn:aws:iam::00000000000:role/windmill-stage"]
    }
  }
}

resource "aws_iam_role" "ec2_ro" {
  name = "ec2_ro"
  path = "/windmill-stage/w=infra/"
  assume_role_policy = data.aws_iam_policy_document.wmill_sub_arp.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"]
}
```

The intent here is that in that the `ec2_ro` role is created in the
`/windmill-stage/` path, and can be assumed by the `windmill-stage`
role, which in turn can be assumed by the k8s `windmill` service
acount in EKS via
[IRSA](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html). 

With that done, the service account can assume any other role that is
in the path/namespace starting with `/windmill-stage/`. 

This script creates a convention where the namespace of `w=infra` maps
to the windmill "infra" workspace in this example. By creating any
number of "w=<workspace>" mappings, we can create roles that have
various permissions (including e.g. roles that span accounts for
cross-account actions).

With this, all roles that are expected to be available to a particular
workspace, e.g. `infra` has the `ec2_ro` role, will appear in a
variable in a folder in the `infra` workspace in windmill, and all
members of the infra workspace can use those privileges to query ec2
APIs, to the extent allowed by the managed policy associated above
(the managed `AmazonEC2ReadOnlyAccess` policy in this case).

The idea is that a service team can be granted access to AWS resources
via temporary, expiring tokens that the entire team doesn't have to do
any work to leverage automatically rotated secrets with limited permissions.

An example could be a windmill script like this from the `infra` workspace:

```python
import os
import wmill
import boto3
import json

def main(region_name: str):
    """A main function is required for the script to be able to accept arguments.
    Types are recommended."""
    creds = json.loads(wmill.get_variable("f/aws/iam"))['ec2_ro']['Credentials']
    print(f"creds are {creds}")
    s = boto3.session.Session(
      region_name=region_name, 
      aws_access_key_id=creds['AccessKeyId'], 
      aws_secret_access_key=creds['SecretAccessKey'], 
      aws_session_token=creds['SessionToken'])
    reservations = s.client('ec2').describe_instances()['Reservations']
    instances = list()
    for r in reservations:
      for i in r['Instances']:
        instances.append(i['InstanceId'])
    return {region_name: instances} 
    # the return value is then parsed and can be retrieved by other scripts conveniently
```

The temporary (expiring) credentials for the `ec2_ro` iam role is provided in the `f/aws/iam` variable as a json blob which is extracted and used 
to authenticate and return the instance IDs in a region.

