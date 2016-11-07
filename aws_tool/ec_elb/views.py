import sys
sys.path.append('/data/awstool/aws_tool/aws_api')

from django.shortcuts import render
from django.http import HttpResponse
from django.template import *
from ge_aws import ec2_list, get_load_balancer, ec2_vpc_list, ec2_subnet_list, ec2_search, ec2_tag, get_lb_status
from collections import defaultdict

def index(request):
	return render(request, 'ec_elb/index.html', {})

def get_elb(request):
	if 'account' in request.GET and request.GET['account'] != '':
		current_profile = request.GET['account'].strip()

		if current_profile == 'annmoon':
			console = "https://ap-northeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-northeast-1"
		else:
			console = "https://ap-southeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-southeast-1"

	else:
		current_profile = 'default'
		console = "https://ap-southeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-southeast-1"

	#lb_namne = 'backoffice'
	response = get_load_balancer(current_profile)
	elbs = response['LoadBalancerDescriptions']

	#all_dict = {}
	all_list = []

	for elb in elbs:
		ins_dict = {}

		for ins in elb['Instances']:
			ins_list = []
			tag = ec2_tag('default', ins['InstanceId'])
			ins_list.append(tag)

			status = get_lb_status(str(elb['LoadBalancerName']), str(ins['InstanceId']), current_profile)
			ins_list.append(status)
			ins_dict[ins['InstanceId']] = ins_list

		l = []
		l.append(elb['LoadBalancerName'])
		l.append(elb['DNSName'])
		l.append(ins_dict)
		l.append(elb['HealthCheck'])

		all_list.append(l)


	#all_dict['elb'] = all_list

	return render(request, 'ec_elb/list.html', {'data' : all_list, 'current_profile' : current_profile, 'console_url' : console})
