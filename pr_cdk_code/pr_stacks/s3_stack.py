from aws_cdk import (
    aws_s3 as s3,
    aws_ssm as ssm,
    core
)

class S3Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        # using account_id in bucket name because buckets have to
        # be globally unique.  We dont NEED to use account id
        account_id = core.Aws.ACCOUNT_ID

        self.lambda_bucket = s3.Bucket(self, id=f'{env_name}-lambda-bucket',
                                  access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                  encryption=s3.BucketEncryption.S3_MANAGED,
                                  bucket_name=f'{env_name}-{account_id}-lambda-deploy-packages',
                                  block_public_access=s3.BlockPublicAccess(
                                      block_public_acls=True,
                                      block_public_policy=True,
                                      ignore_public_acls=True,
                                      restrict_public_buckets=True
                                  ),
                                  removal_policy=core.RemovalPolicy.DESTROY # RETAIN
                                  )

        core.CfnOutput(self,id='lambda_bucket_id',
            value=self.lambda_bucket.bucket_name,
            export_name='lambda-bucket'
        )

        ssm.StringParameter(self, id=f"{env_name}-ssm-lambda-bucket",
                            parameter_name=f'/{env_name}/lambda-s3-bucket',
                            string_value=self.lambda_bucket.bucket_name
                            )



        frontend_bucket=s3.Bucket(self, "frontend",
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            bucket_name=f'{env_name}-' + account_id+'-'+env_name+'-frontend',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            ),
            removal_policy=core.RemovalPolicy.DESTROY

        )

        core.CfnOutput(self,'s3-frontend-export',
            value=frontend_bucket.bucket_name,
            export_name='frontend-bucket'
        )

        #CloudTrail Bucket

        self.cloudtrail_bucket=s3.Bucket(self, "cloudtrail",
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            bucket_name=f'{env_name}-' + account_id+'-'+env_name+'-cloudtrail',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            ),
            removal_policy=core.RemovalPolicy.DESTROY

        )
