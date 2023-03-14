import boto3
import openpyxl

def update_tags():
    workbook = openpyxl.load_workbook('ec2data.xlsx')
    worksheet = workbook['Sheet1']
    column1 = worksheet['A']
    column2 = worksheet['B']
    column3 = worksheet['C']


    for i in range(0, len(column1)):
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(column1[i].value)
        instance.create_tags(
            Tags=[
                {
                    'project_Code':column3[i].value,
                    'Environment': column2[i].value,
                },
            ]
        )
    
update_tags()