#!/usr/bin/env python3

from aws_cdk import core
from aws_cdk import aws_s3 as s3
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
from pr_stacks.cdn_stack import CDNStack
from pr_stacks.codepipeline_frontend import CodePipelineFrontendStack
from pr_stacks.aws101a_stack import AWS101A


app = core.App()

env_name = app.node.try_get_context('env')


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
lambda_stack = LambdaStack(app, id='lambda-stack', vpc=vpc_stack.vpc, lambdasg=security_stack.lambda_sg, lambdarole=security_stack.lambda_basic_role)
lambda_stack.create_s3_trigger(source_bucket_name=f'{env_name}-cdk-rds-event-bucket', lambda_ref=lambda_stack.my_rds_lambda, events=[s3.EventType.OBJECT_CREATED], prefix='test_rds_', suffix='.csv')


cdn_stack = CDNStack(app, id='cdn-stack', s3Bucket=core.Fn.import_value('frontend-bucket'))
cp_frontend_stack = CodePipelineFrontendStack(app, id='cp-fe-stack', webhostingbucket=core.Fn.import_value('frontend-bucket'))

aws_101a_stack = AWS101A(app, id='aws101a-stack')


# synth will synthesis the cloudformation template
app.synth()
