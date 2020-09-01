# Udemy: Ultimate DevOps using AWS CDK - 100% Hands-On (with Python)

https://www.udemy.com/course/aws-devops-professional-cdk-serverless/learn/lecture/19951400#questions/11175273

## Setup

mkdir <projectdir>
cd <projectdir>
cdk init app --language python

python3 -m venv .env


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

## References

### AWS Docs

https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html

### AWS Aurora Serverless Database / Lambda

https://aws.amazon.com/getting-started/hands-on/building-serverless-applications-with-amazon-aurora-serverless/

### CDK Examples

https://github.com/aws-samples/aws-cdk-examples

## Layers

```text
mkdir layers_temp
cd layers_temp
mkdir requests_layer
cd requests_layer
pip install requests -t .
cd ..
zip -r9 ../pr_cdk_code/py_layers/requests_layer.zip .

```
