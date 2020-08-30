echo "vpc-stack"
cdk deploy vpc-stack --profile spr --force

echo 'security-stack'
cdk deploy security-stack --profile spr --force

echo 'bastion-stack'
cdk deploy bastion-stack --profile spr --force

echo 'kms-stack'
cdk deploy kms-stack --profile spr --force

echo 's3-stack'
cdk deploy s3-stack --profile spr --force

echo 'rds-stack'
cdk deploy rds-stack --profile spr --force

echo 'redis-stack'
cdk deploy redis-stack --profile spr --force

echo 'cognito-stack'
cdk deploy cognito-stack --profile spr --force

echo 'apigw-stack'
cdk deploy apigw-stack --profile spr --force

echo 'lambda-stack'
cdk deploy lambda-stack --profile spr --force

echo 'cdn-stack'
cdk deploy cdn-stack --profile spr --force

echo 'codepipeline-frontend-stack'
cdk deploy cp-fe-stack --profile spr --force


