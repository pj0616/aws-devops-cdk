
Aug 26:  Pick up at ApiGateway

# to deploy all of the stacks
cdk deploy "*" --profile spr


# when deploying lambda make sure to execute
# it will create s3 bucket for lambda build asses
cdk bootstrap --profile spr


# Code Commit
# Code used for FrontEnd project
# https://github.com/aws-samples/create-react-app-auth-amplify
# IAM Git Credentials
# https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-gc.html?icmpid=docs_acc_console_connect_np
