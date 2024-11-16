#!/bin/bash -e

export AWS_REGION=eu-central-1

echo "Fetching the VPC ID associated with your EKS cluster."
vpc_id=$(aws eks describe-cluster \
  --name "xtreamly-api" \
  --region "$AWS_REGION" \
  --query "cluster.resourcesVpcConfig.vpcId" \
  --output "text")

echo "Retrieving the CIDR range for the VPC of your EKS cluster."
cidr_range=$(aws ec2 describe-vpcs \
  --vpc-ids "$vpc_id" \
  --query "Vpcs[].CidrBlock" \
  --output "text" \
  --region "$AWS_REGION")

echo "Creating a security group for your Amazon EFS mount points."
security_group_id=$(aws ec2 create-security-group \
  --group-name "XtreamlyAPIEfsSecurityGroup" \
  --description "Xtreamly API EFS security group" \
  --vpc-id "$vpc_id" \
  --region "$AWS_REGION" \
  --output "text")

echo "Creating an inbound rule on the new security group that allows NFS traffic from the CIDR for your cluster's VPC."
aws ec2 authorize-security-group-ingress \
  --group-id "$security_group_id" \
  --protocol "tcp" \
  --port "2049" \
  --region "$AWS_REGION" \
  --cidr "$cidr_range"

echo "Creating the Amazon EFS File System for your cluster."
file_system_id=$(aws efs create-file-system \
  --region "$AWS_REGION" \
  --encrypted \
  --tags "Key=Name,Value=xtreamly-api-efs" \
  --performance-mode "generalPurpose" \
  --query "FileSystemId" \
  --output "text")

echo "Waiting for EFS to become available..."
while true; do
  STATUS=$(aws efs describe-file-systems \
    --file-system-id "$file_system_id" \
    --region "$AWS_REGION" \
    --query 'FileSystems[0].LifeCycleState' \
    --output text)

  if [ "$STATUS" == "available" ]; then
    echo "EFS is now available."
    break
  fi

  echo "EFS status: $STATUS. Waiting for 5 seconds..."
  sleep 5
done

echo "Creating an EFS mount target in each of the cluster VPC's subnets."
for subnet in $(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$vpc_id" --region "$AWS_REGION" --query 'Subnets[*].SubnetId' --output text)
do
  aws efs create-mount-target \
  --file-system-id $file_system_id \
  --subnet-id $subnet \
  --region $AWS_REGION \
  --security-groups $security_group_id
done

echo "Creating Access Point for EFS ID: $EFS_ID..."
access_point_id=$(aws efs create-access-point \
  --file-system-id "$file_system_id" \
  --posix-user Uid=0,Gid=0 \
  --root-directory "Path=/,CreationInfo={OwnerUid=0,OwnerGid=0,Permissions=0777}" \
  --query 'AccessPointId' \
  --output text)

echo "Place the below in ./cluster/efs.yaml as value of 'volumeHandle' under 'PersistentVolume'"
echo $file_system_id::$access_point_id