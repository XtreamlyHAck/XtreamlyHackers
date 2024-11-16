#!/bin/bash -e

export CLUSTER_VPC=$(aws eks describe-cluster --name xtreamly-api --region ${AWS_REGION} --query "cluster.resourcesVpcConfig.vpcId" --output text)
export CLUSTER_NAME=xtreamly-api

helm repo add eks https://aws.github.io/eks-charts
helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
    --set clusterName=${CLUSTER_NAME} \
    --set serviceAccount.create=false \
    --set region=${AWS_REGION} \
    --set vpcId=${CLUSTER_VPC} \
    --set serviceAccount.name=aws-load-balancer-controller \
    -n kube-system