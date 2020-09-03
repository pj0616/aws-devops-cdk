from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ssm as ssm
from utils import cdk_utils
import pr_config as cdk_config


class VPCStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context('env')
        print(prj_name, env_name)

        self.vpc = ec2.Vpc(self, id=f'{env_name}VPC',
                           cidr='172.32.0.0/16', # 65536 available addresses in vpc
                           max_azs=2, # max availability zones
                           enable_dns_hostnames=True, # enable public dns address, and gives EC2 ato-assign dns host names to instances
                           enable_dns_support=True, # 0.2 dns server is used, use Amazon DNS server
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   name="Public",
                                   subnet_type=ec2.SubnetType.PUBLIC,   # has internet gateway associated.
                                                                        # resources are accessible from the internet
                                                                        # resources can access internet
                                   cidr_mask=24 # means a subnet mask of: 255.255.255.0 meaning there
                                                # are 251  usable IP addresses in the PUBLIC subnet
                               ),
                               ec2.SubnetConfiguration(
                                   name="Private",
                                   subnet_type=ec2.SubnetType.PRIVATE,
                                                                # nat gateway attached
                                                                # resource can access the internet
                                                                # resources ARE NOT accessible from internet
                                   cidr_mask=24
                               ),
                               ec2.SubnetConfiguration(
                                   name="Isolated",
                                   subnet_type=ec2.SubnetType.ISOLATED,
                                                                # no nat or internet gateway
                                                                # no access to or from internet
                                                                # databases are good candidates for ISOLATED
                                                                # only other AWS resources can access
                                                                # isolated resources
                                   cidr_mask=24
                               )
                           ],
                           nat_gateways=1   # always provisioned in public subnet.
                                            # should be same as azs for failure
                           )

        # get private subnets
        # there will be 2 public, private and isolated subnets
        # because of the max_azs parameter
        priv_subnets = [subnet.subnet_id for subnet in self.vpc.private_subnets]

        # Update the Parameter Store to save application variables
        for i, priv_subnet_id in enumerate(priv_subnets):
            ssm.StringParameter(self, id=f'private-subnet-{i+1}',
                                string_value=priv_subnet_id,
                                parameter_name=f'/{env_name}/private-subnet-{i+1}'
                                )

        cdk_utils.add_tags(self.vpc, cdk_config.email)