# Udemy: Ultimate DevOps using AWS CDK - 100% Hands-On (with Python)

https://www.udemy.com/course/aws-devops-professional-cdk-serverless/learn/lecture/19951400#questions/11175273


## Deploying

In the lectures he is deploying named stacks

`cdk deploy vpc-stack --profile spr`

`cdk deploy security-stack --profile spr`

`cdk deploy bastion-stack --profile spr`

`ssh -i pryan-spr3.pem ec2-user@54.81.30.189`

`cdk deploy kms-stack --profile spr`

`cdk deploy s3-stack --profile spr`

`cdk deploy rds-stack --profile spr`

`cdk deploy redis-stack --profile spr`

`cdk deploy cognito-stack --profile spr`

`cdk bootstrap --profile spr`
