#!/usr/bin/python

# Quick script that alerts on iptable logs
# You must set these things:
# ------------------------------
# (1) User and password of SMTP Server, if using GMAIL insure using unsecure app settings
# (2) Recipients of the SMS need to be in list format
# (3) Email addr must use proper SMS format per company .. ex ATT= txt.att.net

import smtplib
import os 
import time
import argparse
import sys
from Common import TaskController
from Common import Helpers

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

global Source_IP_List


Source_IP_List = []




#HTML needs to be un "#""


def cli_parser():
	 parser = argparse.ArgumentParser(add_help=False, description='''This script will monito a iptables log and alert by SMS,
	 	(1) Please ensure you provided User-Name and Password for SMTP for SMS.
	 	(2) Provide opitional Iptables log 
	 	(3) Use Gmail for your email provider
	 	''')
	 parser.add_argument(
        "-l", action='store_true', help="List the current Modules Loaded")
	 parser.add_argument("-t", metavar="10", type=int, default=10, help="Will tell how long between log checks in Secs, defaults to 10 Secs.")
	 parser.add_argument("-s", metavar="10", type=int, default=100, help="Max SMS texts that can recived before it shuts down, default is 100.")
	 parser.add_argument("-e", metavar="email@eamil.com", help="Set required email addr user, ex ale@email.com")
	 parser.add_argument("-p", metavar="1234", help="Set required email password")
	 parser.add_argument("-r", metavar="alex@gmail.com,a@yahoo.com", help="Set the Recipients")
	 parser.add_argument("-log", metavar="/var/log/iptables.log", default="/var/log/iptables.log", help="Set a log to parse")
	 parser.add_argument('-h', '-?', '--h', '-help', '--help', action="store_true", help=argparse.SUPPRESS)
	 args = parser.parse_args()
	 if args.h: 
			parser.print_help()
			sys.exit()
	 return args.l, args.t, args.s, args.e, args.p, args.r, args.log

def smtp_check(senders_email, senders_password):
	#Try a conncetion to GMAIL's server to test cred
	try: 
		mail = smtplib.SMTP('smtp.gmail.com', 587)
		mail.ehlo()
		mail.starttls()
		mail.login(senders_email, senders_password)
		mail.quit
	except smtplib.SMTPConnectError as error:
		print "[*] Error occurred during establishment of a connection with the server."
		exit()
	except smtplib.SMTPAuthenticationError as error:
		print "[*] SMTP AUthentication error Plese Check Email and Password and Try again!"
		exit()


def mail(text_alert, max_sms, senders_email, senders_password): 
	global sms
	recipient = ['xx@txt.att.net']
	#recipient = ['xx@txt.att.net', 'xx@tmomail.net']

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "ADT-ALERT"
	msg['From'] = senders_email
	msg['To'] = ", ".join(recipient)

# Create the body of the message (a plain-text and an HTML version).
	text = text_alert
	
	#HTML SUPPORT LIVES HERE
	#html = """\
	#<html>
	 # <head></head>
		#<body>
		 # <p>BECON HAS LANDEDbr>
			#</p>
		#</body>
	#</html>
	#"""

# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	#part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
	msg.attach(part1)
	#msg.attach(part2)

# Send the message via local SMTP server.
	mail = smtplib.SMTP('smtp.gmail.com', 587)
	mail.ehlo()
	mail.starttls()
	mail.login(senders_email, senders_password)
	mail.sendmail(senders_email, recipient, msg.as_string())
	mail.quit()
	print "[*] Message has been sent!"
	sms_check(max_sms)
	return max_sms


#This function monitors the log file 
def syslog_mon(sleep_time, max_sms, senders_email, senders_password, iptables_log):
	#Use log_file to point to the log you need to monitor
		while True:
			try:
				f = open(iptables_log, "r")
				try:
				# OR read one line at a time.
					log_data = f.readlines()
					f.close()	
					Alert_on = ''	
					for Alert_on in log_data:
						trigger = "CALLBACK"
						if trigger in Alert_on:
							Listed_data = str(Alert_on)
							Listed_data  = Listed_data.split()
							data=''
						for element in Listed_data:
							if "SRC" in element:
								SRC_IP=element
								#Now check IP to see if it has been sent yet.
								ip_check(SRC_IP, max_sms, senders_email, senders_password)
								break
				except IOError:
					pass
			except IOError:
				pass
			sleep(sleep_time)

#This function will check to see if the IP SMS has been sent yet, or add it the dict
def ip_check(SRC_IP, max_sms, senders_email, senders_password): 
	if SRC_IP in Source_IP_List:
		return
	else:
		Source_IP_List.append(SRC_IP)
		print "[*] We Have a CALLBACK at:", SRC_IP
		mail(SRC_IP, max_sms, senders_email, senders_password)
		clear_file()
	return



#Open and clear th file for future Alets
def clear_file():
	try:
		f = open("/var/log/iptables.log", "w+")
		f.write("")
		f.close()
		print "[*] File has been cleared"
	except IOError:
		pass  

def sms_check(max_sms):
	max_sms = max_sms - 1
	if max_sms <= 1:
		print "[*] Reached max SMS count"
		exit()
	else:
		print "[*]", max_sms, "SMS remaing"
		return max_sms
	

 #Sleep so you wont block file   
def sleep(how_long):
	 print "[*] Sleeping for interval of:", how_long, "second(s)"
	 time.sleep(how_long)
	



def main():
	Helpers.title()
	cli_list, cli_time, cli_sms, cli_user, cli_pass, cli_recp, cli_log = cli_parser()
 	Task = TaskController.Conducter()
 	if cli_list:
		Task.ListModules()
		exit()

	#Performing checks to ensure proper delivery of SMS messages.
	if cli_recp is None:
		print "[*] missing Recipients... Now quiting"
		exit()
	if cli_user is None:
		print "[*] missing User-Name for SMTP login.. Now quiting"
		exit()
	if cli_pass is None:
		print "[*] missing Password for SMTP login.. Now quiting"
		exit()
	if cli_log == "/var/log/iptables.log":
		print "[*] WARNING Defualt log path is being used"
	#Try to connect to your SMTP server
	smtp_check(cli_user, cli_pass)
	syslog_mon(cli_time, cli_sms, cli_user, cli_pass, cli_log)


if __name__ == "__main__":
	try:	
		main()
	except KeyboardInterrupt:
		print 'Interrupted'
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

