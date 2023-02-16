import json
import boto3

client = boto3.client('dynamodb')
def lambda_handler(event, context):
    print(event['queryParams']['id'])
    response = client.get_item(
            TableName='apidata',
            Key={
                'id': {
                    'S': event['queryParams']['id']
                }
            }
        )

    return response