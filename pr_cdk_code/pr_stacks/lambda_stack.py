from aws_cdk import (
    aws_lambda as lb,
    aws_apigateway as apigw,
    aws_lambda_event_sources as lambda_events,
    aws_s3 as s3,
    core,
)


class LambdaStack(core.Stack):

    def create_s3_trigger(self, source_bucket_name: str, lambda_ref: lb.Function, events: list=None, prefix: str='',
                          suffix: str='') -> None:
        """
        Seems hard to believe, but you cannot use 'from_bucket_name' to get a reference to the bucket, but that
        returns an IBucket, and the S3EventSource wants a Bucket.

        see: https://github.com/aws/aws-cdk/issues/4323
        see: https://gitter.im/awslabs/aws-cdk?at=5d1a6821ddd2c007c7441c21

        :param source_bucket_name:
        :param lambda_ref:
        :param events:
        :param prefix:
        :param suffix:
        :return:
        """
        if events is None:
            events = [s3.EventType.OBJECT_CREATED]

        # I would rather create this bucket in the S3 stack, but if it is going to be an event source
        # then I need the actual bucket... sucks..
        source_bucket = s3.Bucket(self, id='pryan-lambda-event-bucket',
                                  access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
                                  encryption=s3.BucketEncryption.S3_MANAGED,
                                  bucket_name=source_bucket_name,
                                  block_public_access=s3.BlockPublicAccess(
                                      block_public_acls=True,
                                      block_public_policy=True,
                                      ignore_public_acls=True,
                                      restrict_public_buckets=True
                                  ),
                                  removal_policy=core.RemovalPolicy.DESTROY # RETAIN
                                  )

        # source_bucket = s3.Bucket.from_bucket_name(self, id='src_bucket', bucket_name=source_bucket_name)

        filters = [s3.NotificationKeyFilter(prefix=prefix, suffix=suffix)]
        s3_trigger = lambda_events.S3EventSource(bucket=source_bucket, events=events, filters=filters)
        s3_trigger.bind(lambda_ref)

        # lambda_ref.add_event_source(source=lambda_events.S3EventSource(source_bucket,
        #                                                                events=events,
        #                                                                filters=[s3.NotificationKeyFilter(prefix=prefix, suffix=suffix)]
        #                                                                )
        #                             )


    def __init__(self, scope: core.Construct, id: str,vpc, lambdasg, lambdarole, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_function = lb.Function(self, 'helloworldfunction',
                                      runtime=lb.Runtime.PYTHON_3_8,
                                      code=lb.Code.asset('pr_hello_lambda'),
                                      handler='hello.handler',
                                      security_group=lambdasg,
                                      vpc=vpc,
                                      role=lambdarole
                                      )

        # https://stackoverflow.com/questions/63585965/cdk-python-lambda-gets-bundled-every-time-i-run-a-cdk-command
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3_assets.README.html
        my_ip_lambda = lb.Function(self, "MyLambda",
                                       runtime=lb.Runtime.PYTHON_3_8,
                                       handler="hello_ip.handler",
                                        security_group=lambdasg,
                                        vpc=vpc,
                                        code=lb.Code.from_asset(
                                           'pr_ip_lambda',
                                           bundling=core.BundlingOptions(
                                               image=lb.Runtime.PYTHON_3_8.bundling_docker_image,
                                               command=[
                                                   'bash', '-c',
                                                   'pip install -r requirements.txt -t /asset-output && cp -au . /asset-output'
                                               ],
                                           )
                                       ),
                                   role=lambdarole
                            )

        self.my_rds_lambda = lb.Function(self, "MyRDSLambda",
                                       runtime=lb.Runtime.PYTHON_3_8,
                                       handler="rds_lambda.handler",
                                    security_group=lambdasg,
                                    vpc=vpc,
                                    code=lb.Code.from_asset(
                                           'pr_rds_lambda',
                                           bundling=core.BundlingOptions(
                                               image=lb.Runtime.PYTHON_3_8.bundling_docker_image,
                                               command=[
                                                   'bash', '-c',
                                                   'pip install -r requirements.txt -t /asset-output && cp -au . /asset-output'
                                               ],
                                           )
                                       ),
                                    role=lambdarole,
                                         timeout=core.Duration.minutes(3)
                                    )

        api_gateway2 = apigw.LambdaRestApi(self, 'iplambda',
                                          handler=my_ip_lambda,
                                          rest_api_name='myiplambdaapi'
                                          )


        # NOTE - we are using LambdaRestApi.  This will setup a
        # api gateway resource that uses a Lambda Proxy
        api_gateway = apigw.LambdaRestApi(self, 'helloworld',
                                          handler=lambda_function,
                                          rest_api_name='mylambdaapi'
                                          )

