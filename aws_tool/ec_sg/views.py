import sys
sys.path.append('/data/awstool/aws_tool/aws_api')

from django.shortcuts import render
from django.http import HttpResponse
from django.template import *
from ge_aws import ec2_list, get_load_balancer, ec2_vpc_list, ec2_subnet_list, ec2_search, ec2_sg



# Create your views here.
def index(request):
	return render(request, 'ec_sg/index.html', {})


# ec2 all list
def get_ec2_list(request):
	all_ec2 = ec2_list('default')
	ec2 = all_ec2['Reservations']
	return render(request, 'ec_sg/ec2_list.html', {'data' : ec2, 'sg_list': ['.001', '.002', '.003', '.004'] })


# ec2 search list
def get_ec2_search(request):

	filters = []

	if 'ins' in request.GET and request.GET['ins'] != '':
		status = [request.GET['ins'].strip()]
		current_status = request.GET['ins'].strip()
		f1 = {'Name':'instance-state-code', 'Values':status}
		filters.append(f1)
	else:
		status = []
		current_status = ''


	if 'vpc' in request.GET and request.GET['vpc'] != '':
		vpc = [request.GET['vpc'].strip()]
		current_vpc = request.GET['vpc'].strip()
		f2 = {'Name':'vpc-id', 'Values':vpc}
		filters.append(f2)
	else:
		vpc = []
		current_vpc = ''


	if 'subnet' in request.GET and request.GET['subnet'] != '':
		subnet = [request.GET['subnet'].strip()]
		current_subnet = request.GET['subnet'].strip()
		f3 = {'Name':'subnet-id', 'Values':subnet}
		filters.append(f3)
	else:
		subnet = []
		current_subnet = ''


	if 'account' in request.GET and request.GET['account'] != '':
		current_profile = request.GET['account'].strip()

		if current_profile == 'annmoon':
			console = "https://ap-northeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-northeast-1"
		else:
			console = "https://ap-southeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-southeast-1"

	else:
		current_profile = 'default'
		console = "https://ap-southeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-southeast-1"

	


	vpc_all_list = ec2_vpc_list(current_profile)
	vpc_list = vpc_all_list['Vpcs']

	subnet_all_list = ec2_subnet_list(current_profile, *vpc)
	subnet_list = subnet_all_list['Subnets']


	all_ec2_dic = ec2_search(current_profile,*filters)
	all_ec2_list = all_ec2_dic['Reservations']

	return render(request, 'ec_sg/ec2_list.html', {
		'data' : all_ec2_list, 
		'sg_list': ['.001', '.002', '.003', '.004'], 
		'vpcs' : vpc_list, 
		'subnets' : subnet_list, 
		'current_status' : current_status, 
		'current_vpc' : current_vpc, 
		'current_subnet' : current_subnet,
		'current_profile' : current_profile,
		'console_url' : console,
	})



def get_sg_list(request):

	if 'account' in request.GET and request.GET['account'] != '':
		current_profile = request.GET['account'].strip()

		if current_profile == 'default':
			console = "https://ap-northeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-northeast-1"
		else:
			console = "https://ap-southeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-southeast-1"

	else:
		current_profile = 'default'
		console = "https://ap-southeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-southeast-1"


	all_sg_dict = ec2_sg(current_profile)
	all_sg_list = all_sg_dict['SecurityGroups']

	return render(request, 'ec_sg/sg_list.html', {
		'data' : all_sg_list, 
		'sg_list': ['.001', '.002', '.003', '.004'], 
		'current_profile' : current_profile,
		'console_url' : console,
	})


def get_ec2_search_test(request):

	filters = []

	if 'ins' in request.GET and request.GET['ins'] != '':
		status = [request.GET['ins'].strip()]
		current_status = request.GET['ins'].strip()
		f1 = {'Name':'instance-state-code', 'Values':status}
		filters.append(f1)
	else:
		status = []
		current_status = ''


	if 'vpc' in request.GET and request.GET['vpc'] != '':
		vpc = [request.GET['vpc'].strip()]
		current_vpc = request.GET['vpc'].strip()
		f2 = {'Name':'vpc-id', 'Values':vpc}
		filters.append(f2)
	else:
		vpc = []
		current_vpc = ''


	if 'subnet' in request.GET and request.GET['subnet'] != '':
		subnet = [request.GET['subnet'].strip()]
		current_subnet = request.GET['subnet'].strip()
		f3 = {'Name':'subnet-id', 'Values':subnet}
		filters.append(f3)
	else:
		subnet = []
		current_subnet = ''


	if 'account' in request.GET and request.GET['account'] != '':
		current_profile = request.GET['account'].strip()

		if current_profile == 'annmoon':
			console = "https://ap-northeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-northeast-1"
		else:
			console = "https://ap-southeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-southeast-1"

	else:
		current_profile = 'default'
		console = "https://ap-southeast-1.console.aws.amazon.com/ec2/v2/home?region=ap-southeast-1"

	


	vpc_all_list = ec2_vpc_list(current_profile)
	vpc_list = vpc_all_list['Vpcs']

	subnet_all_list = ec2_subnet_list(current_profile, *vpc)
	subnet_list = subnet_all_list['Subnets']


	all_ec2_dic = ec2_search(current_profile,*filters)
	all_ec2_list = all_ec2_dic['Reservations']

	return render(request, 'ec_sg/ec2_list2.html', {
		'data' : all_ec2_list, 
		'sg_list': ['.001', '.002', '.003', '.004'], 
		'vpcs' : vpc_list, 
		'subnets' : subnet_list, 
		'current_status' : current_status, 
		'current_vpc' : current_vpc, 
		'current_subnet' : current_subnet,
		'current_profile' : current_profile,
		'console_url' : console,
	})


