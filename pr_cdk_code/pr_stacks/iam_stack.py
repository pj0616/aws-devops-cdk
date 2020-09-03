from aws_cdk import core
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ssm as ssm

class IAMStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        env_name = self.node.try_get_context('env')
        dyn_db = self.node.try_get_context('dynamodb-arn')

        self.lambda_basic_role = iam.Role(self,
                                'lambdabasicrole',
                                assumed_by=iam.ServicePrincipal(service='lambda.amazonaws.com'),
                                role_name=f'{env_name}-cdk-lambda-role',
                                managed_policies=[
                                    iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')
                                    ]
                                )

        # self.lambda_basic_role.add_to_policy(
        #     statement=iam.PolicyStatement(actions=['dynamodb:PutItem'],
        #                                   resources=[dyn_db])
        # )
        self.lambda_basic_role.add_to_policy(
            statement = iam.PolicyStatement(actions=['s3:*', 'rds:*'],
                                        resources=['*'])
        )


        ssm.StringParameter(self, f'{env_name}-lambdarole-arn-param',
                            parameter_name=f"/{env_name}/lambda-role-arn",
                            string_value=self.lambda_basic_role.role_arn
                            )
        ssm.StringParameter(self, f'{env_name}-lambdarole-name-param',
                            parameter_name=f"/{env_name}/lambda-role-name",
                            string_value=self.lambda_basic_role.role_name
                            )