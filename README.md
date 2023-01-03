# authn-iam ECS Demo <!-- omit in toc -->

A demonstration using @cyberark Conjur's authn-iam integration with AWS ECS

- [Pre-Requisites](#pre-requisites)
- [Setup](#setup)
- [Configuration of ECS Task Definition](#configuration-of-ecs-task-definition)
- [Running the ECS Task](#running-the-ecs-task)

## Pre-Requisites

* [AWS ECS](https://aws.amazon.com/ecs/)
* [Conjur](https://conjur.org/)

## Setup

1. [Create and enable authn-iam authenticator in Conjur.](https://docs.cyberark.com/Product-Doc/OnlineHelp/AAM-DAP/Latest/en/Content/Operations/Services/AWS_IAM_Authenticator.htm)
2. [Create IAM Role for ECS Task Definition "Task Role".](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html#create_task_iam_policy_and_role)
3. [Create Conjur Host Identity reflecting IAM Role created in Step 2.](https://docs.cyberark.com/Product-Doc/OnlineHelp/AAM-DAP/Latest/en/Content/Operations/Services/AWS_IAM_Authenticator.htm#mc-dropdown-bodyf15b6975-450c-4fc6-9677-0b2b86693fa8)
4. Build Dockerfile to Docker container. \
   `$ docker build -t authn-iam-ecs-demo .`
5. [Deploy Docker image created in Step 4 to AWS Elastic Container Repository.](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html)

## Configuration of ECS Task Definition

* [Create ECS Task Definition.](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-definitions.html)

Be sure the IAM Role created in Step 2 is attached to the ECS Task Definition.

Include the following environment variables in the Task Definition for the container to use. __Values provided are examples and should be replaced with values relevant to your environment__:
    
```
AWS_ROLE_ARN=arn:aws:iam::123456789012:role/TaskRole
CONJUR_APPLIANCE_URL=https://conjur-host.example.com
CONJUR_ACCOUNT=account
CONJUR_AUTHN_LOGIN=host/authn-iam-ecs-demo
CONJUR_AUTHN_IAM_SERVICE_ID=service-id
SECRET_ID=secret-id
VALIDATE_CERT=true
```

## Running the ECS Task

* [Run ECS Task.](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/run-task.html)

The ECS Task will run the container image and output the result to the console.