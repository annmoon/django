import boto3
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

def send_mail_boto3(to_addr, message):
	session = boto3.Session(profile_name='annemail')
	client = session.client('ses', region_name='us-west-2')
	to_emails = to_addr
	msg = MIMEMultipart('alternative')
	msg['From'] = 'LDAP <noreply@annmoon.com>'
	msg['To'] = ",".join(to_emails)
	msg['Subject'] = 'LDAP Password reset'

	html_part = MIMEText(message, 'html')
	msg.attach(html_part)

	response = client.send_raw_email(
		Source=msg['From'], 
		Destinations=to_emails,
		RawMessage={
			'Data': msg.as_string()
		},
	)

	return response
