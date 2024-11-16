#!/bin/bash -e

# Assign arguments to variables
DOCKER_DIR=$1
IMAGE_NAME=$2

aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin 893048150390.dkr.ecr.${AWS_REGION}.amazonaws.com

docker buildx create --use
docker build --platform linux/amd64 -t ${IMAGE_NAME} ${DOCKER_DIR}

docker tag ${IMAGE_NAME}:latest 893048150390.dkr.ecr.${AWS_REGION}.amazonaws.com/xtreamly-api/${IMAGE_NAME}:latest
docker push 893048150390.dkr.ecr.${AWS_REGION}.amazonaws.com/xtreamly-api/${IMAGE_NAME}:latest