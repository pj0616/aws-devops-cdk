from aws_cdk import aws_ec2 as ec2
from aws_cdk import core


class BastionStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, sg: ec2.SecurityGroup, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.bastion_host = ec2.Instance(self, id='pryan-bastion-host',
                                         instance_type=ec2.InstanceType(instance_type_identifier='t2.micro'),
                                         machine_image=ec2.AmazonLinuxImage(
                                             edition=ec2.AmazonLinuxEdition.STANDARD,
                                             generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                             virtualization=ec2.AmazonLinuxVirt.HVM,
                                             storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                            ),
                                         vpc=vpc,
                                         key_name='pryan-spr3',  # must create the key name manually first
                                                                # this is the pem private/public key
                                         vpc_subnets=ec2.SubnetSelection( # this will create the ec2 instance in one of the PUBLIC subnets of the VPC that we just defined above
                                             subnet_type=ec2.SubnetType.PUBLIC
                                         ),
                                         security_group=sg
                                         )

