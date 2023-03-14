import boto3

#get the data from text file
def updatetags():
    with open('data.txt', 'r') as f:
        instance_ids = f.read()
    ec2 = boto3.resource('ec2')
    for i in range (0,len(instance_ids)):
        instance = ec2.Instance(instance_ids[i])
        instance.create_tags(Tags=[{'Key': 'Name', 'Value': 'test'}])
        print(instance_ids[i])
