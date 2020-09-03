from aws_cdk import (
    aws_cognito as cognito,
    aws_iam as iam,
    aws_ssm as ssm,
    core
)


class CognitoStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        user_pool2 = cognito.UserPool(self, id=f'{env_name}-precog',
                                      auto_verify=cognito.AutoVerifiedAttrs(
                                              email=True
                                          ),
                                      sign_in_aliases=cognito.SignInAliases(
                                          email=True,
                                          phone=True
                                      ),
                                      self_sign_up_enabled=True,
                                      user_pool_name=f'{env_name}-cdk-2-user-pool',
                                      custom_attributes={
                                          "param1":cognito.StringAttribute(mutable=True)
                                      },
                                      password_policy=cognito.PasswordPolicy(
                                          min_length=10,
                                          require_lowercase=True,
                                          require_digits=True,
                                          require_symbols=False,
                                          require_uppercase=True
                                      )
                                      )


        user_pool = cognito.CfnUserPool(self, id=f'{env_name}-cognito-user-pool',
                                        auto_verified_attributes=[
                                            'email'
                                        ],
                                        username_attributes=[
                                            'email', 'phone_number'
                                        ],
                                        user_pool_name=f'{env_name}-cdk-user-pool',
                                        schema=[
                                            {
                                                "attributeDataType": "String",
                                                "name": "param1",
                                                "mutable": True
                                            }
                                        ],
                                        policies=cognito.CfnUserPool.PoliciesProperty(
                                            password_policy=cognito.CfnUserPool.PasswordPolicyProperty(
                                                minimum_length=10,
                                                require_lowercase=True,
                                                require_numbers=True,
                                                require_symbols=False,
                                                require_uppercase=True
                                            )
                                        )
                                        )

        user_pool_client2 = cognito.UserPoolClient(self, id=f'{env_name}-pool-client2',
                                                   user_pool=user_pool2,
                                                   user_pool_client_name=f'{env_name}-cdk-app-client2'
                                                   )
        identity_pool2 = cognito.CfnIdentityPool(self, id=f'{env_name}-identify-pool-2',
                                                allow_unauthenticated_identities=False,
                                                cognito_identity_providers=[
                                                    cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                                                        client_id=user_pool_client2.user_pool_client_id,
                                                        provider_name=user_pool.attr_provider_name
                                                    )
                                                ],
                                                identity_pool_name=f'{env_name}-cdk-identity-pool2'
                                                )

        user_pool_client = cognito.CfnUserPoolClient(self, id=f'{env_name}-pool-client',
                                                     user_pool_id=user_pool.ref,
                                                     client_name=f'{env_name}-cdk-app-client'
                                                     )

        identity_pool = cognito.CfnIdentityPool(self, id=f'{env_name}-identify-pool',
                                                allow_unauthenticated_identities=False,
                                                cognito_identity_providers=[
                                                    cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                                                        client_id=user_pool_client.ref,
                                                        provider_name=user_pool.attr_provider_name
                                                    )
                                                ],
                                                identity_pool_name=f'{env_name}-cdk-identity-pool'
                                                )


        ssm.StringParameter(self, id='app-id',
                            parameter_name=f"/{env_name}/cognito-app-client-id",
                            string_value=user_pool_client.ref
                            )

        ssm.StringParameter(self, id='user-pool-id',
                            parameter_name=f"/{env_name}/cognito-user-pool-id",
                            string_value=user_pool_client.user_pool_id
                            )

        ssm.StringParameter(self, id='identity-pool-id',
                            parameter_name=f"/{env_name}/cognito-identity-pool-id",
                            string_value=identity_pool.ref  # ref returns the id
                            )
