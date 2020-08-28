echo 'lambda-stack'
cdk destroy lambda-stack --profile spr --force

echo 'apigw-stack'
cdk destroy apigw-stack --profile spr --force

echo 'cognito-stack'
cdk destroy cognito-stack --profile spr --force

echo 'redis-stack'
cdk destroy redis-stack --profile spr --force

echo 'rds-stack'
cdk destroy rds-stack --profile spr --force

echo 's3-stack'
cdk destroy s3-stack --profile spr --force

echo 'kms-stack'
cdk destroy kms-stack --profile spr --force

echo 'bastion-stack'
cdk destroy bastion-stack --profile spr --force

echo 'security-stack'
cdk destroy security-stack --profile spr --force

echo "vpc-stack"
cdk destroy vpc-stack --profile spr --force
