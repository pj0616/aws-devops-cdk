from aws_cdk import core
from pr_stacks.vpc_stack import VPCStack
from pr_stacks.iam_stack import IAMStack
from pr_stacks.securitygroup_stack import SecurityGroupStack

class AppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # vpc = VPCStack(scope, 'pryan-vpc')
        # iam_stack = IAMStack(scope, 'pryan-iam')
        # security_stack = SecurityGroupStack(scope, 'pryan-sg', vpc=vpc.vpc)
        #
        # self.sub_stacks = [vpc, iam_stack, security_stack]