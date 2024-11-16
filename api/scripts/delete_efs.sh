#!/bin/bash -e

export AWS_REGION=eu-central-1
EFS_NAME="xtreamly-api-efs"

echo "Finding EFS ID for name: $EFS_NAME..."
EFS_ID=$(aws efs describe-file-systems \
  --region "$AWS_REGION" \
  --query "FileSystems[?Tags[?Key=='Name' && Value=='$EFS_NAME']].FileSystemId" \
  --output text)

echo "Deleting Access Points for EFS ID: $EFS_ID..."
ACCESS_POINT_IDS=$(aws efs describe-access-points \
  --file-system-id "$EFS_ID" \
  --region "$AWS_REGION" \
  --query 'AccessPoints[*].AccessPointId' \
  --output text)

for AP_ID in $ACCESS_POINT_IDS; do
  echo "Deleting Access Point: $AP_ID..."
  aws efs delete-access-point \
    --access-point-id "$AP_ID" \
    --region "$AWS_REGION"
done

echo "Deleting Mount Targets for EFS ID: $EFS_ID..."
MOUNT_TARGET_IDS=$(aws efs describe-mount-targets \
  --file-system-id "$EFS_ID" \
  --region "$AWS_REGION" \
  --query 'MountTargets[*].MountTargetId' \
  --output text)

for MT_ID in $MOUNT_TARGET_IDS; do
  echo "Deleting Mount Target: $MT_ID..."
  aws efs delete-mount-target \
    --mount-target-id "$MT_ID" \
    --region "$AWS_REGION"
done

echo "Waiting for Mount Targets to be deleted..."
while true; do
  REMAINING_MOUNT_TARGETS=$(aws efs describe-mount-targets \
    --file-system-id "$EFS_ID" \
    --region "$AWS_REGION" \
    --query 'MountTargets' \
    --output text)

  if [ -z "$REMAINING_MOUNT_TARGETS" ]; then
    echo "All Mount Targets deleted."
    break
  fi

  echo "Waiting for 5 seconds..."
  sleep 5
done

echo "Deleting EFS ID: $EFS_ID..."
aws efs delete-file-system \
  --file-system-id "$EFS_ID" \
  --region "$AWS_REGION"

echo "EFS $EFS_ID and associated resources have been deleted."