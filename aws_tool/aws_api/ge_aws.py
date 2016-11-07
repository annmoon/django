#!/usr/bin/python
# Filename: ge_aws.py

import boto3
from ge_session import create_session
import re


## return all ec2 list as dictionary type.
def ec2_list(p="default"):
    s = create_session(p)
    ec2 = s.client('ec2')

    return ec2.describe_instances()

def ec2_search(p="default", *args):
    s = create_session(p)
    ec2 = s.client('ec2')

    if not args:
        return ec2.describe_instances()
    else:
        return ec2.describe_instances(Filters=args)


## return load_balancer
def get_load_balancer(p="default", *l_name):
    s = create_session(p)
    lb = s.client('elb')

    if not l_name:
        elb = lb.describe_load_balancers()
    else:
        elb = lb.describe_load_balancers(LoadBalancerNames=l_name)

    return elb


## return status of load_balancer
def get_lb_status(l_name, ins_id, p="default"):
    s = create_session(p)
    lb = s.client('elb')
    
    response = lb.describe_instance_health(LoadBalancerName=l_name, Instances=[ {'InstanceId': ins_id} ])

    if len(response['InstanceStates']) == 1:
        elb_status = response['InstanceStates'][0]['State']


    return elb_status


def ec2_vpc_list(p="default"):
    s = create_session(p)
    ec2 = s.client('ec2')

    return ec2.describe_vpcs()


def ec2_subnet_list(p="default", *vpcid):
    s = create_session(p)
    ec2 = s.client('ec2')

    if vpcid:
        filters = [{'Name':'vpc-id', 'Values':vpcid}]
        return ec2.describe_subnets(Filters=filters)
    else:
        return ec2.describe_subnets()


# return SG
def ec2_sg(p="default", *sg_id):
    s = create_session(p)
    ec2 = s.client('ec2')
    security_group = ec2.describe_security_groups(GroupIds=sg_id)

    return security_group


# return ec2 instance tag name
def ec2_tag(p="default", *ec2_id):
    s = create_session(p)
    ec2 = s.client('ec2')
    response = ec2.describe_instances(Filters=[{'Name':'instance-id','Values':ec2_id}])

    tag_name = ''
    if len(response['Reservations']) == 1:
        ins = response['Reservations'][0]['Instances']

        if len(ins) == 1:
            tags = ins[0]['Tags']

            for t in tags:
                if t['Key'] == 'Name':
                    tag_name = t['Value']
                    break

    return tag_name

