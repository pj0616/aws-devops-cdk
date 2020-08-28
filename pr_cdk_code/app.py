#!/usr/bin/env python3

from aws_cdk import core
from pr_stacks.vpc_stack import VPCStack
from pr_stacks.securitygroup_stack import SecurityGroupStack
from pr_stacks.bastion_stack import BastionStack
from pr_stacks.kms_stack import KMSStack
from pr_stacks.s3_stack import S3Stack
from pr_stacks.rds_stack import RDSStack
from pr_stacks.redis_stack import RedisStack
from pr_stacks.cognito_stack import CognitoStack
from pr_stacks.apigw_stack import APIStack
from pr_stacks.lambda_stack import LambdaStack

app = core.App()
# PrCdkCodeStack(app, "pr-cdk-code")
vpc_stack = VPCStack(app, id='vpc-stack')
security_stack = SecurityGroupStack(app, id='security-stack', vpc=vpc_stack.vpc)
bastion_stack = BastionStack(app, id='bastion-stack', vpc=vpc_stack.vpc, sg=security_stack.bastion_sg)
kms_stack = KMSStack(app, id='kms-stack')
s3_stack = S3Stack(app, id='s3-stack')
rds_stack = RDSStack(app, id='rds-stack', vpc=vpc_stack.vpc, lambdasg=security_stack.lambda_sg, bastionsg=security_stack.bastion_sg, kmskey=kms_stack.kms_rds)
redis_stack = RedisStack(app, id='redis-stack', vpc=vpc_stack.vpc, redissq=security_stack.redis_sg)
cognito_stack = CognitoStack(app, id='cognito-stack')
apigw_stack = APIStack(app, id='apigw-stack')

# make sure to bootstrap
# cdk bootstrap --profile spr
# cdk detected that I was referencing python 3.8 docker and downloaded
#  Pulling from amazon/aws-sam-cli-build-image-python3.8
lambda_stack = LambdaStack(app, id='lambda-stack')

# synth will synthesis the cloudformation template
app.synth()
