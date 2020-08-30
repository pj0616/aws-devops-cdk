echo "vpc-stack"
cdk deploy vpc-stack --profile spr --require-approval never

echo 'security-stack'
cdk deploy security-stack --profile spr --require-approval never

echo 'bastion-stack'
cdk deploy bastion-stack --profile spr --require-approval never

echo 'kms-stack'
cdk deploy kms-stack --profile spr --require-approval never

echo 's3-stack'
cdk deploy s3-stack --profile spr --require-approval never

echo 'rds-stack'
cdk deploy rds-stack --profile spr --require-approval never

echo 'redis-stack'
cdk deploy redis-stack --profile spr --require-approval never

echo 'cognito-stack'
cdk deploy cognito-stack --profile spr --require-approval never

echo 'apigw-stack'
cdk deploy apigw-stack --profile spr --require-approval never

echo 'lambda-stack'
cdk deploy lambda-stack --profile spr --require-approval never

echo 'cdn-stack'
cdk deploy cdn-stack --profile spr --require-approval never

echo 'codepipeline-frontend-stack'
cdk deploy cp-fe-stack --profile spr --require-approval never


