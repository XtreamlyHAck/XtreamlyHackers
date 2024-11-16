#!/bin/bash -e

export AWS_REGION=eu-central-1
eksctl delete cluster -f cluster/create-fargate.yaml
./scripts/delete_efs.sh