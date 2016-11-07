import sys
sys.path.append('/data/awstool/aws_tool/aws_api')

from ge_aws import ec2_sg
from django import template
from django.template.defaultfilters import stringfilter
import boto3

register = template.Library()

#@register.simple_tag
@register.simple_tag
def check_old_vpc(*sg_id):
	client = boto3.client('ec2')

	all_sg = client.describe_security_groups(GroupIds=sg_id)
	sg = all_sg['SecurityGroups']
	num = 0

	if sg_id != '' :
		for i in sg:
			if 'IpPermissions' in i:
				for k in i['IpPermissions']:
					if 'IpRanges' in k:
						for j in k['IpRanges']:
							if "CidrIp" in j:
								if "10.1.0.0/16" in j['CidrIp']:
									num = num + 1

	if num > 0:
		content = "(Old VPC CIDR 10.1.0.0/16 still exist)"
	else:
		content = " "
	
	return content


@register.filter(name='check_vpc')
def check_vpc(sg_id):
	all_sg = ec2_sg("default", sg_id)
	sg = all_sg['SecurityGroups']

	return sg