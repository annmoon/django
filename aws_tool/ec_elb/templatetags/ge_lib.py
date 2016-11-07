import sys
sys.path.append('/data/awstool/aws_tool/aws_api')
from django import template
from ge_aws import ec2_tag, get_lb_status
import boto3
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.simple_tag(name='get_ec2_tag')
@stringfilter
def get_ec2_tag(ec2_id, profile):
    tag = ec2_tag(profile, ec2_id)
    return tag

@register.filter(name='get_lb_status_name')
def get_lb_status_name(ec2_id, args):
    if args is None:
        return False

    arg_list = [arg.strip() for arg in args.split(',')]

    status_name = get_lb_status(str(arg_list[0]), ec2_id, str(arg_list[1]))
    return status_name