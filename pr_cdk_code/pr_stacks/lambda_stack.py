from aws_cdk import (
    aws_lambda as lb,
    aws_apigateway as apigw,
    core,
)


class LambdaStack(core.Stack):

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

        my_rds_lambda = lb.Function(self, "MyRDSLambda",
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
                                    role=lambdarole
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

