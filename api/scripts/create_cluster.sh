#!/bin/bash -e

export AWS_REGION=eu-central-1

echo "!!!!!!!!!!!!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!!!!!!!!!!!!!"
echo "You must enable STS in ${AWS_REGION} for load balancer creation go here: https://console.aws.amazon.com/iam/home#/account_settings"
echo "!!!!!!!!!!!!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!!!!!!!!!!!!!"

eksctl create cluster -f ./cluster/create-fargate.yaml
aws eks update-kubeconfig --name xtreamly-api

echo "Setting up alb..."
./scripts/setup_lb.sh
echo "alb created"

echo "Setting up efs..."
./scripts/create_efs.sh
echo "efs created"

echo "Take the value shown from the previous command fs-<XYZ>::fsap-<XYZ>"
echo "Place it in ./cluster/efs.yaml as value of 'volumeHandle' under 'PersistentVolume'"

kubectl create secret generic fastapi-secret --from-env-file=.env -n xtreamly-api
