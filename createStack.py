import boto3
import time
import sys

client = boto3.client('cloudformation')

# replace first parameter with the SHA value of the commit
#create parameters from arguments
parameters_list = []
web_app_name = {"ParameterKey" : "WebAppName", "ParameterValue" : sys.argv[2]}
parameters_list.append(web_app_name)
web_app_dep_name = {"ParameterKey" : "WebAppDepName", "ParameterValue"  : sys.argv[3]}
parameters_list.append(web_app_dep_name)
web_app_tag = {"ParameterKey" : "WebAppEC2Tag", "ParameterValue"  : sys.argv[4]}
parameters_list.append(web_app_tag)

with open("template.json","r") as file:
        stack = client.create_stack(StackName="Stack"+sys.argv[1],TemplateBody=file.read(), Parameters=parameters_list )

print(stack["StackId"])

progress = client.describe_stacks(StackName=stack["StackId"])
progress = progress["Stacks"][0]["StackStatus"]

if str(progress) != "CREATE_COMPLETE":
        i=0
        while  i == 0:
                progress = client.describe_stacks(StackName=stack["StackId"])
                progress = progress["Stacks"][0]["StackStatus"]
                if progress == "CREATE_COMPLETE" :
                        i = 1
                if progress == "DELETE_IN_PROGRESS":
                        raise StopIteration("Error: Stack is being deleted.")
                print("waiting for stack to complete")
                if progress == "ROLLBACK_IN_PROGRESS":
                        raise StopIteration("Error: Stack is rolling back, something is wrong.")
                print(progress)
                time.sleep(10)

print("Stack is now created!")






