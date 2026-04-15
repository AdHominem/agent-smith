from aws_cdk import (
    Stack, aws_lambda as lambda_,
    aws_apigateway as apigateway,
)
from constructs import Construct

class AgentSmithStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        chat_fn = lambda_.Function(
            self, "ChatFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="handler.main",
            code=lambda_.Code.from_asset("src/chat"),
        )

        api = apigateway.RestApi(self, "ChatApi", rest_api_name="agent-smith-api")

        chat = api.root.add_resource("chat")
        chat.add_method("POST",
                        apigateway.LambdaIntegration(chat_fn),
                        authorization_type=apigateway.AuthorizationType.IAM)
