#!/bin/bash -e

export AWS_REGION=eu-central-1

create_ecr_repository() {
  local repo=$1

  # Create the ECR registry if not exists
  aws ecr describe-repositories --repository-names xtreamly-api/${repo} --region ${AWS_REGION} >/dev/null 2>&1 || \
  aws ecr create-repository --repository-name xtreamly-api/${repo} --region ${AWS_REGION}
}

create_ecr_repository "api"
create_ecr_repository "streamer"

./scripts/push_docker_image.sh ./server api
./scripts/push_docker_image.sh ./streamer streamer
#kubectl create secret generic fastapi-secret --from-env-file=.env -n xtreamly-api
kubectl apply -f ./cluster/efs.yaml
kubectl apply -f ./cluster/deploy-streamer.yaml
kubectl apply -f ./cluster/deploy-api.yaml
