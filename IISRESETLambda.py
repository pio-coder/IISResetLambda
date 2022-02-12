#!/usr/bin/python

import boto3
import sys
import time
import json

def start_web_server_services(instances, session):

    # locate all running instances
    RunningInstances = [webserver.id for webserver in instances]

    # print the instances for logging purposes
    # print RunningInstances
    if RunningInstances:
        print("The following running instances were identified as WS")
        print(RunningInstances)
    
        ssm_client = session.client('ssm')
    
        response = ssm_client.send_command(
            InstanceIds= RunningInstances,
            DocumentName='AWS-RunPowerShellScript',
            TimeoutSeconds=30,
            Parameters={
                'commands': [
                    #'iisreset /START',
                    'ipconfig'
                ]
            },
        )
        print(RunningInstances)
        command_id = response['Command']['CommandId']
    
        response = ssm_client.list_commands(CommandId=command_id)
        print("response")
    
        while response['Commands'][0]['Status'] != "Success":
            if response['Commands'][0]['Status'] == "Failed":
                sys.exit(1)
            else:
                time.sleep(1)
                response = ssm_client.list_commands(CommandId=command_id)
        print(response)
    else:
        print("No running instances were identified as WS")


def lambda_handler(event, context):

        session = boto3.Session()
        ec2_client = session.resource('ec2')
        ssm_client = session.client('ssm')
        
        filters = [
           {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
        
        instances = ec2_client.instances.filter(Filters=filters)
        
        for status in ec2_client.meta.client.describe_instance_status()['InstanceStatuses']:
            print(status)
       
