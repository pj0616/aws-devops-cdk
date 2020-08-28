echo 'lambda-stack'
cdk destroy lambda-stack --profile spr

echo 'apigw-stack'
cdk destroy apigw-stack --profile spr

echo 'cognito-stack'
cdk destroy cognito-stack --profile spr

echo 'redis-stack'
cdk destroy redis-stack --profile spr

echo 'rds-stack'
cdk destroy rds-stack --profile spr

echo 's3-stack'
cdk destroy s3-stack --profile spr

echo 'kms-stack'
cdk destroy kms-stack --profile spr

echo 'bastion-stack'
cdk destroy bastion-stack --profile spr

echo 'security-stack'
cdk destroy security-stack --profile spr

echo "vpc-stack"
cdk destroy vpc-stack --profile spr
