import json
import os
import boto3
from aws_lambda_powertools import Logger

GUARDRAIL_ID = os.environ['GUARDRAIL_ID']
MODEL_ID = os.environ['MODEL_ID']

bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get('AWS_REGION', 'eu-central-1'))

logger = Logger()

@logger.inject_lambda_context
def main(event, context):
    try:
        body = json.loads(event.get('body', "{}"))
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {"Content-Type": "application/json"},
            'body': json.dumps({"error": "Invalid JSON in request body"})
        }

    message = body.get('message', "")

    logger.info("Received message: %s", message)

    # Commented out until model quota is clarified

    # Invoke Bedrock Model
    #response = bedrock.invoke_model(
    #    modelId=MODEL_ID,
    #    body=json.dumps({
    #        "messages": [
    #            {"role": "user", "content": [{"text": message}]}
    #        ]
    #    })
    #)

    #response_body = json.loads(response["body"].read())
    #reply = response_body["output"]["message"]["content"][0]["text"]

    #logger.info("Agent response: %s", reply)

    return {
        'statusCode': 200,
        'headers': {"Content-Type": "application/json"},
        'body': json.dumps({"reply": f"Echo: {message}"})
    }