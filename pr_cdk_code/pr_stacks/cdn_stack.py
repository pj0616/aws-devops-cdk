from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cdn,
    aws_ssm as ssm,
    core
)

class CDNStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, s3Bucket, **kwargs):
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        bucketName = s3.Bucket.from_bucket_name(self, 's3bucket', s3Bucket)

        cdn_id = cdn.CloudFrontWebDistribution(self, id='webhosting-cdn',
            origin_configs=[cdn.SourceConfiguration(
                behaviors=[
                    cdn.Behavior(is_default_behavior=True)
                ],
                origin_path="/build",
                s3_origin_source=cdn.S3OriginConfig(
                    s3_bucket_source=bucketName,
                    origin_access_identity=cdn.OriginAccessIdentity(self, id='wehosting-origin')
                )
            )],
            error_configurations=[
                cdn.CfnDistribution.CustomErrorResponseProperty(
                    error_code=400,
                    response_code=200,
                    response_page_path="/"
                ),
                cdn.CfnDistribution.CustomErrorResponseProperty(
                    error_code=403,
                    response_code=200,
                    response_page_path="/"
                ),
                cdn.CfnDistribution.CustomErrorResponseProperty(
                    error_code=404,
                    response_code=200,
                    response_page_path="/"
                )
            ]
        )

        ssm.StringParameter(self, id='cdn-dist-id',
                            parameter_name=f"/{env_name}/app-distribution-id",
                            string_value=cdn_id.distribution_id
                            )

        ssm.StringParameter(self, id='cdn-url',
                            parameter_name=f"/{env_name}/app-cdn-url",
                            string_value=f'https://{cdn_id.domain_name}'  # url
                            )