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

#### Layers Example

https://github.com/aws-samples/aws-cdk-examples/blob/master/python/lambda-ddb-mysql-etl-pipeline/etl_pipeline_cdk/etl_pipeline_cdk_stack.py
https://blog.skbali.com/2018/11/aws-lambda-layer-example-in-python/

## Layers
NOTE: the directory MUST be called `python`.  The zipfile can be named anything, but the zipfile name is what you reference in CDK


```text
cd $HOME 
mkdir -p temp/python 
cd temp/python
docker run --rm -it -v "$PWD":/var/task lambci/lambda:build-python3.8 bash 
pip install pymysql -t .
pip install requests -t .
cd ..
zip -r9 <zipfilename>.zip python

```

## SFTP AWS Transfer

`sftp -i ~/.ssh/aws_transfer_key cdkuser@s-a4960f7e50534ac9b.server.transfer.us-east-1.amazonaws.com`

