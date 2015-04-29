import smtplib
import os 
import time
import argparse
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

global Source_IP_List





def mail(): 
  global sms

  senders_email = "xxxxx@gmail.com"
  senders_password = "xxxxx"

  recipient = ['11111111@vtext.com', '1234567890@txt.att.net']]

  # Create message container - the correct MIME type is multipart/alternative.
  msg = MIMEMultipart('alternative')
  msg['Subject'] = "ALERT"
  msg['From'] = senders_email
  msg['To'] = ", ".join(recipient)

# Create the body of the message (a plain-text and an HTML version).
  text = "This sucks"
  
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



def main():
  while True:
    mail()


if __name__ == "__main__":
  main()
