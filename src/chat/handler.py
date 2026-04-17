import json
from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context
def main(event, context):
    logger.info(event)

    body = json.loads(event.get('body', "{}"))
    message = body.get('message', "")
    
    logger.info("Received message: %s", message)

    return {
        'statusCode': 200,
        'headers': {"Content-Type": "application/json"},
        'body': json.dumps({"reply": f"Echo: {message}"})
    }