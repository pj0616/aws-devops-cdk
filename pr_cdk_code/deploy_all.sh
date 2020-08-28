echo "vpc-stack"
cdk deploy vpc-stack --profile spr

echo 'security-stack'
cdk deploy security-stack --profile spr

echo 'bastion-stack'
cdk deploy bastion-stack --profile spr

echo 'kms-stack'
cdk deploy kms-stack --profile spr

echo 's3-stack'
cdk deploy s3-stack --profile spr

echo 'rds-stack'
cdk deploy rds-stack --profile spr

echo 'redis-stack'
cdk deploy redis-stack --profile spr

echo 'cognito-stack'
cdk deploy cognito-stack --profile spr

echo 'apigw-stack'
cdk deploy apigw-stack --profile spr

echo 'lambda-stack'
cdk deploy lambda-stack --profile spr


