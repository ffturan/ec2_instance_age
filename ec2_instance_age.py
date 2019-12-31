#!/usr/bin/env python3

import boto3
import sys
import datetime
from botocore.exceptions import ClientError
from prettytable import PrettyTable

def connect_aws(vvProfile,vvRegion,vvService):
    try:
        boto3.setup_default_session(profile_name=vvProfile,region_name=vvRegion)
        worker = boto3.client(vvService)
        return worker
    except ClientError as e:
        print(e)

def check_args():
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} profile-name region-name')
        exit()


#
# MAIN STARTS HERE
#

if __name__ == '__main__':
    # Check number of arguments
    check_args()
    # Set vars
    vProfile=sys.argv[1]
    vRegion=sys.argv[2]
    # Connect to AWS
    worker_ec2=connect_aws(vProfile,vRegion,'ec2')
    # Get time
    vNow=datetime.datetime.now(datetime.timezone.utc)
    # Pretty Table prepare
    vCuteTableNew=PrettyTable()
    vCuteTableOld=PrettyTable()
    # Empty List
    worker_list=[]
    # Try
    try:
        response = worker_ec2.describe_instances(Filters=[{'Name':'instance-state-name','Values':['running']}])
    except ClientError as e:
        print(e)
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            id_holder=instance["InstanceId"]
            type_holder=instance["InstanceType"]
            ip_holder=instance["PrivateIpAddress"]
            time_holder=instance["LaunchTime"]
            for item in instance["Tags"]:
              if item['Key'] == 'Name':
                  name_holder=item['Value']
            age_holder=vNow - time_holder
            worker_list.append((id_holder,name_holder,type_holder,ip_holder,age_holder))
    newest_list=sorted(worker_list, key=lambda age: age[4])
    oldest_list=sorted(worker_list, key=lambda age: age[4], reverse=True)
    print(f'-----------------------')
    print(f'Newest 10 EC2 Instances')
    print(f'-----------------------')
    vCuteTableNew.field_names = ["ID", "NAME", "TYPE", "IP", "AGE"]
    for item in newest_list[:10]:
        vCuteTableNew.add_row([item[0],item[1],item[2],item[3],item[4]])
    print(vCuteTableNew)
    print(f'-----------------------')
    print(f'Oldest 10 EC2 Instances')
    print(f'-----------------------')
    vCuteTableOld.field_names = ["ID", "NAME", "TYPE", "IP", "AGE"]
    for item in oldest_list[:10]:
        vCuteTableOld.add_row([item[0],item[1],item[2],item[3],item[4]])
    print(vCuteTableOld)
