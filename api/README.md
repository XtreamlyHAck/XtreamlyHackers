# XtreamHacks API

It is a [Fast API](https://fastapi.tiangolo.com/), hosted on [AWS EKS](https://developers.eksworkshop.com/docs/python/eks/).

## Prerequisites

1. awscli: `brew install awscli`
2. eksctl: `brew install eksctl`
3. helm: `brew install helm`
4. libomp: `brew install libomp`
5. postgresql: `brew install postgresql`
6. Setup your AWS credentials locally:
    ```
    $ mkdir ~/.aws
    $ cat >> ~/.aws/config
    [default]
    aws_access_key_id=YOUR_ACCESS_KEY_HERE
    aws_secret_access_key=YOUR_SECRET_ACCESS_KEY
    region=YOUR_REGION (such as us-west-2, us-west-1, etc)
    ```
7. [docker](https://docs.docker.com/get-docker/)
8. [kubectl](https://kubernetes.io/docs/tasks/tools/)

## Local setup

1. `python -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r ./requirements`

## Starting API locally

1. `fastapi dev ./server/main.py`

## Starting Streamer locally

1. `python -m streamer.stream`

## Commands

1. Provision cluster in AWS: `./scripts/create_cluster.sh`
2. Deprovision cluster in AWS: `./scripts/delete_cluster.sh`
3. Deploy FAST API: `./scripts/deploy.sh`


