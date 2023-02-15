import json
import pandas as pd
import boto3

client = boto3.client('dynamodb')
def lambda_handler(event, context):
    # get all items from dynamodb
    response = client.scan(
        TableName='apidata'
    )

    return response
    