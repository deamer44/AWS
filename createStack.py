
import boto3
import time
import sys

client = boto3.client('cloudformation')

# replace first parameter with the SHA value of the commit
with open("template.json","r") as file:
        stack = client.create_stack(StackName="Stack"+sys.argv[1],TemplateBody=file.read())

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
                print("waiting for stack to complete")
                print(progress)
                time.sleep(10)

print("Stack is now created!")








