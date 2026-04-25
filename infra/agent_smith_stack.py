from aws_cdk import (
    Stack, aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_bedrock as bedrock, Duration,
)
from constructs import Construct

MODEL_ID = "eu.amazon.nova-lite-v1:0"

class AgentSmithStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Layer reference
        powertools_layer = lambda_.LayerVersion.from_layer_version_arn(
            self, "PowertoolsLayer",
            "arn:aws:lambda:eu-central-1:017000801446:layer:AWSLambdaPowertoolsPythonV3-python312-x86_64:7"
        )

        # Define guardrails
        guardrail = bedrock.CfnGuardrail(self, "AgentSmithGuardrail",
                                         name="agent-smith-guardrail",
                                         blocked_input_messaging="I cannot process this message",
                                         blocked_outputs_messaging="I cannot output this message",
                                         content_policy_config=bedrock.CfnGuardrail.ContentPolicyConfigProperty(
                                             filters_config=[
                                                 bedrock.CfnGuardrail.ContentFilterConfigProperty(
                                                     type="HATE",
                                                     input_strength="HIGH",
                                                     output_strength="HIGH"
                                                 ),
                                                 bedrock.CfnGuardrail.ContentFilterConfigProperty(
                                                     type="VIOLENCE",
                                                     input_strength="HIGH",
                                                     output_strength="HIGH"
                                                 ),
                                                 bedrock.CfnGuardrail.ContentFilterConfigProperty(
                                                     type="SEXUAL",
                                                     input_strength="HIGH",
                                                     output_strength="HIGH"
                                                 ),
                                                 bedrock.CfnGuardrail.ContentFilterConfigProperty(
                                                     type="INSULTS",
                                                     input_strength="HIGH",
                                                     output_strength="HIGH"
                                                 ),
                                                 bedrock.CfnGuardrail.ContentFilterConfigProperty(
                                                     type="MISCONDUCT",
                                                     input_strength="HIGH",
                                                     output_strength="HIGH"
                                                 ),
                                                 bedrock.CfnGuardrail.ContentFilterConfigProperty(
                                                     type="PROMPT_ATTACK",
                                                     input_strength="HIGH",
                                                     output_strength="NONE"
                                                 ),
                                             ]
                                         )
                                         )

        # Define Lambda handler
        chat_fn = lambda_.Function(
            self, "ChatFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="handler.main",
            code=lambda_.Code.from_asset("src/chat"),
            layers=[powertools_layer],
            timeout=Duration.seconds(30),
            environment={
                "MODEL_ID": MODEL_ID,
                "GUARDRAIL_ID": guardrail.attr_guardrail_id,
                "GUARDRAIL_VERSION": "1"
            }
        )

        # Define API Gateway
        api = apigateway.RestApi(self, "ChatApi", rest_api_name="agent-smith-api")

        chat = api.root.add_resource("chat")
        chat.add_method("POST",
                        apigateway.LambdaIntegration(chat_fn),
                        authorization_type=apigateway.AuthorizationType.IAM)

        # Set Policy
        chat_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel", "bedrock:ApplyGuardrail"],
            resources=[
                f"arn:aws:bedrock:{self.region}::foundation-model/*",
                f"arn:aws:bedrock:{self.region}:{self.account}:inference-profile/*",
                guardrail.attr_guardrail_arn
            ]
        ))