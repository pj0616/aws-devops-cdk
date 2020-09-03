from aws_cdk import (
    aws_ssm as ssm,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as sm,
    core
)
import json


class RDSStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, lambdasg: ec2.SecurityGroup,
                 bastionsg: ec2.SecurityGroup, kmskey, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        creds_json_template = {'username': 'admin'}

        db_creds = sm.Secret(self, id="db-secret",
                             secret_name=f'{env_name}-rds-secret',
                             generate_secret_string=sm.SecretStringGenerator(
                                 include_space=False,  # no space in secret
                                 password_length=12,
                                 generate_string_key='rds-password',  # key in json dictionary for the password
                                 exclude_punctuation=True,
                                 secret_string_template=json.dumps(creds_json_template)
                             )
                             )

        db_name = f'pryancdkdb'
        db_mysql = rds.DatabaseCluster(self, id=f'{env_name}-mysql',
                                       default_database_name=db_name,
                                       engine=rds.DatabaseClusterEngine.aurora_mysql(
                                           version=rds.AuroraMysqlEngineVersion.VER_5_7_12
                                       ),
                                       master_user=rds.Login(username='admin',
                                                             password=db_creds.secret_value_from_json('rds-password')),
                                       instance_props=rds.InstanceProps(
                                           vpc=vpc,
                                           vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED),
                                           # will pick one of the isolated Subnets from the vpc
                                           instance_type=ec2.InstanceType(instance_type_identifier='t3.small')
                                       ),
                                       instances=1,
                                       storage_encrypted=True,
                                       storage_encryption_key=kmskey,
                                        removal_policy=core.RemovalPolicy.DESTROY
                                       )

        # we need to define the ingress rules for rds
        db_mysql.connections.allow_default_port_from(lambdasg, 'Access from Lambda Functions')
        db_mysql.connections.allow_default_port_from(bastionsg, "Access from bastion host")

        # ssm
        ssm.StringParameter(self, id=f'{env_name}-db-host',
                            parameter_name=f"/{env_name}/db-host",
                            string_value=db_mysql.cluster_endpoint.hostname
                            )

        ssm.StringParameter(self, id=f'{env_name}-db-name',
                            parameter_name=f"/{env_name}/db-name",
                            string_value=db_name
                            )

        # ssm.StringParameter(self, 'db-endpoint',
        #     parameter_name='/'+env_name+'/db-endpoint',
        #     string_value=db_mysql.cluster_endpoint
        # )
        # ssm.StringParameter(self, 'db-read-endpoint',
        #     parameter_name='/'+env_name+'/db-read-endpoint',
        #     string_value=db_mysql.cluster_read_endpoint
        # )
