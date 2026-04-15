import json


def main(event, context):
    body = json.loads(event.get('body', "{}"))
    message = body.get('message', "")

    return {
        'statusCode': 200,
        'headers': {"Content-Type": "application/json"},
        'body': json.dumps({"reply": f"Echo: {message}"})
    }