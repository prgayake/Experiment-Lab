import boto3
import json

def list_s3_buckets():
    # Create an S3 client
    s3 = boto3.client('s3')

    # List all S3 buckets
    response = s3.list_buckets()
    #push this bucket into json array
    bucketList=[]
    for bucket in response['Buckets']:
        bucketList.append(bucket['Name'])
    return bucketList


def get_bucket_lifecycle(bucketList):
    # Create an S3 client
    s3 = boto3.client('s3')
    lifecycleList=[]
    for bucket in bucketList:
        try:
            response = s3.get_bucket_lifecycle_configuration(Bucket=bucket)
            # Add bucket Name along with lifecycle configuration
            lifecycleList.append({bucket:response['Rules']})
        except:
            pass
    return lifecycleList


def incorrectPolicy(policyData):
    # Create an S3 client
    incorrectPolicy =[]
    s3 = boto3.client('s3')
    for i in policyData:
        for key in i:
            for j in i[key]:
                if j['Expiration']['Days'] < 7 and j['NoncurrentVersionExpiration']['NoncurrentDays'] < 30:
                    print("Bucket Name: ", key, " has incorrect lifecycle policy")
                    incorrectPolicy.append(key)
                else:
                    print("Bucket Name: ", key, " has correct lifecycle policy")

    return incorrectPolicy 

if __name__ == "__main__":
    data=get_bucket_lifecycle(list_s3_buckets())
    policyData = json.dumps(data, indent=2)
    print(incorrectPolicy(json.loads(policyData)))

