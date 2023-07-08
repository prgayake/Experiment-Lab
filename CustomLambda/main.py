import time
import argparse
from utils import saml_client
from utils.teamcity import teamcity_warning, teamcity_message
from metadata import account_loader



with open('lambda.zip', 'rb') as f:
	zipped_code = f.read()

def create_execution_role(account,region,env,client,product,purpose,counter):
    teamcity_message("region = {region}".format(region=requiredRegion))
    sessionObj = client.create_session(role, requiredAccount["account_number"])
    iam_client = sessionObj.client('iam')
    lambda_client = sessionObj.client('lambda')
    role = iam_client.create_role(
        RoleName='aws-'+account+'-'+region+'-00'+'-'+env+'-rol-'+client+'-'+product+'-LambdaBasicExecutionRole'+str(counter),
        AssumeRolePolicyDocument='''{
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {
                                    "Service": "lambda.amazonaws.com"
                                },
                                "Action": "sts:AssumeRole"
                            }
                        ]
                    }
                '''
    )

    iam_client.attach_role_policy(
    RoleName='aws-'+account+'-'+region+'-00'+'-'+env+'-rol-'+client+'-'+product+'-LambdaBasicExecutionRole'+str(counter),
    PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
    
    )

    iam_client.attach_role_policy(
    RoleName='aws-'+account+'-'+region+'-00'+'-'+env+'-rol-'+client+'-'+product+'-LambdaBasicExecutionRole'+str(counter),
    PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole'
    )
    return role['Role']['Arn']




def create_lambda_function(client,role, requiredAccount, requiredRegion, env,tenent, product, purpose,counter,run_time,SubnetIds,SecurityGroupIds,lambda_handler, dryrun):
    rolearn=create_execution_role(account,region,env,tenent,product,purpose,counter)
    time.sleep(10)
    response=lambda_client.create_function(
        FunctionName='aws-'+account+'-'+region+'-00'+'-'+env+'-lmb-'+tenent+'-'+product+'-'+purpose+'-'+str(counter),
        Runtime=run_time,
        Role= rolearn,
        Handler=lambda_handler,
        Code={
            'S3Bucket': 'pradyumnabucketaws7gw',
        'S3Key': 'lambda.zip'
        },
        Timeout=15,
        MemorySize=128,
        VpcConfig={
            'SubnetIds': SubnetIds,
            'SecurityGroupIds': SecurityGroupIds
        },
        Tags={
            'client': client,
            'env': env,
            'ZS_Project_Code': Project_Code
        }
    )

    return response

def getRequiredAccount(requiredAccountName):
    loader = account_loader.AccountLoader()
    accounts = loader.get_active_accounts()
    requiredAccounts = [x for x in accounts if x["account_number"] == requiredAccountName]
    requiredAccount = requiredAccounts[0]
    print("Required Account {0}({1}: {2})".format(requiredAccount["id"], requiredAccount["account_number"],
                                                  requiredAccount["display_name"]))
    return requiredAccount



account = 'a0123'
region = 'use1'
env = 'p'
client = 'client1'
product = 'cus'
purpose = 'backup-restore'
counter = '07'
run_time = 'python3.9'
SubnetIds = ['subnet-04b9f9e00e27cb055']
SecurityGroupIds = ['sg-0db52f880523e96b7']
lambda_handler = 'lambda.lambda_handler'


print(create_lambda_function(account,region,env,client,product,purpose,counter,run_time,SubnetIds,SecurityGroupIds,lambda_handler,'DB098438943'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username")
    parser.add_argument("-p", "--password")
    parser.add_argument("-l", "--role", default="aws-admins")
    parser.add_argument("-a", "--account", default="783005340583")
    parser.add_argument("-r", "--region", default="us-east-1")
    parser.add_argument("-i", "--env", default="p")
    parser.add_argument("-i", "--tenent", default="shrd")
    parser.add_argument("-s", "--product", default="cus")
    parser.add_argument("-e", "--purpose", default="backup-restore")
    parser.add_argument("-t", "--counter", default="01")
    parser.add_argument("-t", "--run_time", default="python3.9")
    parser.add_argument("-t", "--SubnetIds", default="subnet-04b9f9e00e27cb055")
    parser.add_argument("-t", "--SecurityGroupIds", default="sg-0db52f880523e96b7")
    parser.add_argument("-t", "--lambda_handler", default="lambda.lambda_handler")
    parser.add_argument("-t", "--Project Code", default="DB098ZS893")
    parser.add_argument("-d", "--dryrun", default="True")

    args = parser.parse_args()
    dryrun = args.dryrun == 'True'
    client = saml_client.SAML(args.username, args.password)
    requiredAccount = getRequiredAccount(args.account)
    create_lambda_function(client, args.role, requiredAccount, args.region, args.env, args.tenent, args.product,
                     args.purpose, args.counter,args.run_time,args.SubnetIds,args.SecurityGroupIds,args.lambda_handler, dryrun)