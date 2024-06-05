from datetime import datetime
import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Count items in the Lambda event 
    no_messages = str(len(event['Records']))
    print("Found " +no_messages +" messages to process.")

    for message in event['Records']:
        print(message)

        # Parse message body
        message_body = json.loads(message['body'])

        # Get the DynamoDB table
        table = dynamodb.Table('myurl-prod')

        if message_body['action'] == 'create' or message_body['action'] == 'update':
            # Write or update message in DynamoDB
            response = table.put_item(
                Item={
                    'short_code': message_body['short_url'].split('/')[-1],  # Extract short_code from short_url
                    'is_verified': message_body.get('is_verified', False),  # Assuming the URL is verified when it's created or updated
                    'original_url': message_body['original_url']
                }
            )
            print("Wrote/Updated message to DynamoDB:", json.dumps(response))

        elif message_body['action'] == 'delete':
            # Delete message from DynamoDB
            response = table.delete_item(
                Key={
                    'short_code': message_body['short_url'].split('/')[-1]  # Use short_code as the key for deletion
                }
            )
            print("Deleted message from DynamoDB:", json.dumps(response))