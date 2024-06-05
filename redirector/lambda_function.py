import boto3
import json
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

STATUS_CODE = 'statusCode'
STATUS_DESCRIPTION = 'statusDescription'
HEADERS = 'headers'
BODY = 'body'
CONTENT_TYPE = 'Content-Type'
TEXT_PLAIN = 'text/plain'

def create_response(status_code, status_description, headers, body):
    return {
        STATUS_CODE: status_code,
        STATUS_DESCRIPTION: status_description,
        HEADERS: headers,
        BODY: body
    }

def lambda_handler(event, context):
    # Print the entire event for debugging
    print(f"Received event: {json.dumps(event)}")

    # Check if path is in the event
    if 'path' in event:
        path = event['path'].lstrip('/')  # Remove the leading '/'
        print(f"Extracted path: {path}")
    else:
        print("No path provided.")
        return create_response(400, '400 Bad Request', { CONTENT_TYPE: TEXT_PLAIN }, 'No path provided.')

    try:
        # Get the DynamoDB table
        table = dynamodb.Table('myurl-prod')
        response = table.get_item(Key={'short_code': path})
        print(f"DynamoDB response: {json.dumps(response)}")  # Print the full response
    except ClientError as e:
        print(f"ClientError while accessing the table: {e.response['Error']['Message']}")
        return create_response(500, '500 Internal Server Error', { CONTENT_TYPE: TEXT_PLAIN }, 'Internal ERROR.')
    
    if 'Item' in response:
        original_url = response['Item'].get('original_url')
        is_verified = response['Item'].get('is_verified', "False")

        if is_verified == "True":
            print(f"Redirecting to URL: {original_url}")
            return create_response(302, '302 Found', { 'Location': original_url, CONTENT_TYPE: TEXT_PLAIN }, '')
        else:
            print("URL not verified. Returning HTML with continue button.")
            with open('warning.html', 'r') as file:
                html_body = file.read().replace('{original_url}', original_url)
            return create_response(200, '200 OK', { CONTENT_TYPE: 'text/html' }, html_body)
    else:
        print("URL not found.")
        return create_response(404, '404 Not Found', { CONTENT_TYPE: TEXT_PLAIN }, json.dumps('URL not found.'))