from aws_cdk import (
    aws_sqs as sqs,
    aws_iam as iam,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_event_source,
    core
)
import random, string

class ApiSqsLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        env_name = self.node.try_get_context('env')

        #Create the SQS queue
        queue = sqs.Queue(self, id=f"{env_name}-SQSQueue", queue_name=f"{env_name}-queue")

        #Create the API GW service role with permissions to call SQS
        rest_api_role = iam.Role(
            self,
            id=f"{env_name}-RestAPISQSRole",
            assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSQSFullAccess")]
        )

        #Create an API GW Rest API
        base_api = apigw.RestApi(self, id=f'{env_name}-ApiGW',
                                 rest_api_name=f'{env_name}SQSTestAPI',
                                 api_key_source_type=apigw.ApiKeySourceType.HEADER
        )

        usage_api_key_value = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(40))

        usage_api_key = base_api.add_api_key(id=f'{env_name}-apikey', value=usage_api_key_value)
        usage_plan = base_api.add_usage_plan(id=f'{env_name}-usageplan',
                                             name=f'{env_name}-usageplan',
                                             api_key=usage_api_key,
                                             throttle=apigw.ThrottleSettings(
                                                rate_limit=10,
                                                burst_limit=2
                                             )
        )
        usage_plan.add_api_stage(stage=base_api.deployment_stage)

        #Create a resource named "example" on the base API
        api_resource = base_api.root.add_resource('sqstest')


        #Create API Integration Response object: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_apigateway/IntegrationResponse.html
        integration_response = apigw.IntegrationResponse(
            status_code="200",
            response_templates={"application/json": ""},

        )

        #Create API Integration Options object: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_apigateway/IntegrationOptions.html
        api_integration_options = apigw.IntegrationOptions(
            credentials_role=rest_api_role,
            integration_responses=[integration_response],
            request_templates={"application/json": "Action=SendMessage&MessageBody=$input.body"},
            passthrough_behavior=apigw.PassthroughBehavior.NEVER,
            request_parameters={"integration.request.header.Content-Type": "'application/x-www-form-urlencoded'"},
        )

        #Create AWS Integration Object for SQS: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_apigateway/AwsIntegration.html
        api_resource_sqs_integration = apigw.AwsIntegration(
            service="sqs",
            integration_http_method="POST",
                                # must be ACCOUNT_ID. Just the way URL to SQS is created
            path="{}/{}".format(core.Aws.ACCOUNT_ID, queue.queue_name),
            options=api_integration_options
        )

        #Create a Method Response Object: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_apigateway/MethodResponse.html
        method_response = apigw.MethodResponse(status_code="200")

        #Add the API GW Integration to the "example" API GW Resource
        api_resource.add_method(
            "POST",
            api_resource_sqs_integration,
            method_responses=[method_response],
            api_key_required=True
        )

        #Creating Lambda function that will be triggered by the SQS Queue
        sqs_lambda = _lambda.Function(self,'SQSTriggerLambda',
            handler='sqs_lambda.handler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('pr_sqs_lambda'),
        )

        #Create an SQS event source for Lambda
        sqs_event_source = lambda_event_source.SqsEventSource(queue)

        #Add SQS event source to the Lambda function
        sqs_lambda.add_event_source(sqs_event_source)

        # https://67ixnggm81.execute-api.us-east-1.amazonaws.com/prod/sqstest
        region = core.Aws.REGION
        core.CfnOutput(self,'api-gw-url',
            value='https://' + base_api.rest_api_id + '.execute-api.' + region + '.amazonaws.com/prod/sqstest',
            export_name='api-sqs-gw-url'
        )
        print(f'API Key: {usage_api_key_value}')


        """
        POST https://5h0z5fdov0.execute-api.us-east-1.amazonaws.com/prod/sqstest
        Accept: */*
        Cache-Control: no-cache
        Content-Type: application/json
        x-api-key: uJAxwtfKC268lR1EYN7zO9XU9MQZFPQpaK69XzSw
        
        
        {"key":"value"}

        """