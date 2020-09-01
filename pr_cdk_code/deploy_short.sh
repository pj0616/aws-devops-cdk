echo "vpc-stack"
cdk deploy vpc-stack --profile spr --require-approval never

echo 'security-stack'
cdk deploy security-stack --profile spr --require-approval never

echo 'bastion-stack'
cdk deploy bastion-stack --profile spr --require-approval never

echo 'kms-stack'
cdk deploy kms-stack --profile spr --require-approval never

echo 'rds-stack'
cdk deploy rds-stack --profile spr --require-approval never

echo 'lambda-stack'
cdk deploy lambda-stack --profile spr --require-approval never


