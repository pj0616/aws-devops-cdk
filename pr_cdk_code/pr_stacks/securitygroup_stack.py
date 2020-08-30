from aws_cdk import (
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    core
)
from pr_stacks.iam_stack import IAMStack

class SecurityGroupStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, **kwargs):
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        self.lambda_sg = ec2.SecurityGroup(self, id='lambdasg',
                                      security_group_name='pryan-cdk-lambda-sg',
                                      vpc=vpc,
                                      description='pryan SG for Lambda',
                                      allow_all_outbound=True
                                                            # all output bound traffic is allowed
                                                            # so lambda can reach out to any
                                                            # internet resource
                                           )

        self.bastion_sg = ec2.SecurityGroup(self, id='bastionsg',
                                      security_group_name='pryan-cdk-bastion-sg',
                                      vpc=vpc,
                                      description='pryan SG for Bastion',
                                      allow_all_outbound=True)

        self.redis_sg = ec2.SecurityGroup(self, id='redissg',
                                      security_group_name='pryan-cdk-redis-sg',
                                      vpc=vpc,
                                      description='pryan SG for Redis Cluster',
                                      allow_all_outbound=True
                                                            # all output bound traffic is allowed
                                                            # so lambda can reach out to any
                                                            # internet resource
                                           )



        # add SSH inbound rule
        self.bastion_sg.add_ingress_rule(ec2.Peer.any_ipv4(), # any machine is allowed to ssh
                                         ec2.Port.tcp(22),
                                        description='SSH Access')

        self.redis_sg.add_ingress_rule(self.lambda_sg, connection=ec2.Port.tcp(6379), description='Access from Lambda Functions' )



        # IAM Roles
        self.lambda_basic_role = iam.Role(self,
                                id='lambdabasicrole',
                                assumed_by=iam.ServicePrincipal(service='lambda.amazonaws.com'),
                                role_name='pryan-cdk-lambda-role',
                                managed_policies=[
                                    iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')
                                    ]
                                )

        # inline policies
        # give lambda full access to S3 and RDS
        # actions = all S3 and RDS actions
        # resources = for all S3 objects and all RDS databases
        # Normally I think we would want to tighten that up
        self.lambda_basic_role.add_to_policy(
            statement=iam.PolicyStatement(actions=['s3:*', 'rds:*', 'ssm:*', 'secretsmanager:*', 'ec2:*'],
                                          resources=['*'])
        )


        # SSM Parameters
        ssm.StringParameter(self, id='lambda-sg-param',
                            parameter_name=f'/{env_name}/lambda-sg',
                            string_value=self.lambda_sg.security_group_id)

        ssm.StringParameter(self, id='pryan-lambdarole-arn-param',
                            parameter_name=f"/{env_name}/lambda-role-arn",
                            string_value=self.lambda_basic_role.role_arn
                            )
        ssm.StringParameter(self, id='pryan-lambdarole-name-param',
                            parameter_name=f"/{env_name}/lambda-role-name",
                            string_value=self.lambda_basic_role.role_name
                            )
        # iam_stack = IAMStack(scope, 'pryan-iam-stack')

