from aws_cdk import (
    aws_lambda as lb,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_dynamodb as ddb,
    core,
)


class AWS101A(core.Stack):

    def __init__(self, scope: core.Construct, id: str,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        env_name = self.node.try_get_context('env')

        # https://github.com/aws-samples/aws-cdk-examples/blob/master/python/dynamodb-lambda/dynamodb_lambda/dynamodb_lambda_stack.py
        # DynamoDB
        ddb_table = ddb.Table(self, id=f"{env_name}-aws101-ddb",
            partition_key=ddb.Attribute(
                name="pk",
                type=ddb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # IAM Roles
        self.lambda_basic_role = iam.Role(self,
                                id=f'{env_name}-lambdabasicrole-dynamo',
                                assumed_by=iam.ServicePrincipal(service='lambda.amazonaws.com'),
                                role_name=f'{env_name}-cdk-dynamo-lambda-role',
                                managed_policies=[
                                    iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')
                                    ]
                                )

        # inline policies
        # give lambda full access to S3 and RDS
        # actions = all S3 and RDS actions
        # resources = for all S3 objects and all RDS databases
        # Normally I think we would want to tighten that up
        # See below for a better way
        # self.lambda_basic_role.add_to_policy(
        #     statement=iam.PolicyStatement(actions=['dynamodb:*'],
        #                                   resources=['*'])
        # )

        requests_layer = lb.LayerVersion(
            self, id=f"{env_name}-requests-layer",
            code=lb.AssetCode('./pr_layers/requests_layer.zip'),
            compatible_runtimes=[lb.Runtime.PYTHON_3_6, lb.Runtime.PYTHON_3_7, lb.Runtime.PYTHON_3_8]
        )


        # https://stackoverflow.com/questions/63585965/cdk-python-lambda-gets-bundled-every-time-i-run-a-cdk-command
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3_assets.README.html
        my_dynamodb_lambda = lb.Function(self, id=f"{env_name}-dynamodb-lambda",
                                         runtime=lb.Runtime.PYTHON_3_8,
                                         handler="dynamodb_lambda.handler",
                                         code=lb.AssetCode("pr_dynamo_lambda"),
                                         layers=[requests_layer],
                                         role=self.lambda_basic_role,
                                         timeout=core.Duration.minutes(3)
                            )

        my_dynamodb_lambda.add_environment("DDB_TABLE_NAME", ddb_table.table_name)

        # create inline policy to allow lambda write permission to this table
        ddb_table.grant_write_data(my_dynamodb_lambda)

        api_gateway2 = apigw.LambdaRestApi(self, id=f'{env_name}-api-dynamo-lambda',
                                          handler=my_dynamodb_lambda,
                                          rest_api_name=f'{env_name}-lambda-dyn'
                                          )
