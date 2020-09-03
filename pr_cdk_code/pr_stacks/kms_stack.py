from aws_cdk import (
    aws_kms as kms,
    aws_ssm as ssm,
    core
)

class KMSStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        self.kms_rds = kms.Key(self, id=f'{env_name}-rdskey',
                               description=f"{prj_name}-key-rds",
                               enable_key_rotation=True
                               )

        self.kms_rds.add_alias(
            alias_name=f'alias/{prj_name}-key-rds'
        )

        # create ssm parameter for key
        ssm.StringParameter(self, id=f'{env_name}-rdskey-param',
                            string_value=self.kms_rds.key_id,
                            parameter_name=f'/{env_name}/rds-kms-key'
                            )
