#!/usr/bin/env python3
import base64
from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    core,
)

"""
https://cloudacademy.com/blog/elastic-load-balancers-ec2-auto-scaling-to-support-aws-workloads/

"""

class LoadBalancerStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        env_name = self.node.try_get_context('env')


        vpc = ec2.Vpc(self, id=f"{env_name}VPC")

        data = open("./pr_stacks/httpd.sh", "rb").read()
        httpd=ec2.UserData.for_linux()
        httpd.add_commands(str(data,'utf-8'))


        asg = autoscaling.AutoScalingGroup(
            self,
            id=f"{env_name}-ASG",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            user_data=httpd,
            min_capacity=2,
            max_capacity=5
        )

        lb = elbv2.ApplicationLoadBalancer(
            self, "LB",
            vpc=vpc,
            internet_facing=True)


        """
        Listeners: For every load balancer, regardless of the type used, 
        you must configure at least one listener. The listener defines how your 
        inbound connections are routed to your target groups based on ports 
        and protocols set as conditions. The configurations of the listener 
        itself differ slightly depending on which ELB you have selected.
        """
        listener = lb.add_listener(id=f"{env_name}-Listener", port=80)


        """
        Target Groups: A target group is simply a group of your resources that 
        you want your ELB to route requests to, such as a fleet of EC2 instances. 
        You can configure the ELB with a number of different target groups, each
         associated with a different listener configuration and associated rules. 
         This enables you to route traffic to different resources based upon the 
         type of request.
        """
        listener.add_targets(id=f"{env_name}-Target", port=80, targets=[asg])
        listener.connections.allow_default_port_from_any_ipv4(description="Open to the world")

        asg.scale_on_request_count(id=f"{env_name}-AModestLoad", target_requests_per_second=1)
        core.CfnOutput(self,"LoadBalancer",export_name="LoadBalancer",value=f"http://{lb.load_balancer_dns_name}")
