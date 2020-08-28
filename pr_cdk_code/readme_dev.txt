
Aug 26:  Pick up at ApiGateway

# to deploy all of the stacks
cdk deploy "*" --profile spr


# when deploying lambda make sure to execute
# it will create s3 bucket for lambda build asses
cdk bootstrap --profile spr