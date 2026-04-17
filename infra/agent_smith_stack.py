from aws_cdk import (
    Stack, aws_lambda as lambda_,
    aws_apigateway as apigateway,
)
from constructs import Construct

class AgentSmithStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Layer reference
        powertools_layer = lambda_.LayerVersion.from_layer_version_arn(
            self, "PowertoolsLayer",
            "arn:aws:lambda:eu-central-1:017000801446:layer:AWSLambdaPowertoolsPythonV3-python312-x86_64:7"
        )

        chat_fn = lambda_.Function(
            self, "ChatFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="handler.main",
            code=lambda_.Code.from_asset("src/chat"),
            layers=[powertools_layer],
        )

        api = apigateway.RestApi(self, "ChatApi", rest_api_name="agent-smith-api")

        chat = api.root.add_resource("chat")
        chat.add_method("POST",
                        apigateway.LambdaIntegration(chat_fn),
                        authorization_type=apigateway.AuthorizationType.IAM)
