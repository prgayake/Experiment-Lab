import json
import pandas as pd
import boto3

client = boto3.client('dynamodb')
def lambda_handler(event, context):
    #get id from query string and find in dynamodb table
    id = event['queryParams']['id']
    print(event)
    response = client.get_item(
        TableName='test',
        Key={
            'id': {
                'S': id
            }
        }
    )
    
    return
    {
        'statusCode': 200,
        'body': json.dumps(response)
    }
