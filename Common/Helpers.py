#!/usr/bin/python
import smtplib
import os
import os, sys, types, string, textwrap

def color(string, status=True, warning=False, bold=True, blue=False, firewall=False):
    """
    Change text color for the linux terminal, defaults to green.
    Set "warning=True" for red.
    stolen from Veil :)
    """
    attr = []
    if status:
        # green
        attr.append('32')
    if warning:
        # red
        attr.append('31')
    if bold:
        attr.append('1')
    if firewall:
        attr.append('33')
    if blue:
        #blue
        attr.append('34')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

def Gmail_smtp_check(senders_email, senders_password):
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

def title():
  os.system('clear')
  print " ============================================================"
  print " Curent Version: v1.0 | Website: CyberSyndicates.com"
  print " ============================================================"
  print " Twitter: @real_slacker007 |  Twitter: @Killswitch_gui"
  print " ============================================================"
  print  "  ___ __  __ ___     _                _   _         _   " 
  print  " / __|  \/  / __|___| |   ___  __ _  /_\ | |___ _ _| |_ "
  print  " \__ \ |\/| \__ \___| |__/ _ \/ _` |/ _ \| / -_) '_|  _|"
  print  " |___/_|  |_|___/   |____\___/\__, /_/ \_\_\___|_|  \__|"
  print  "                              |___/                     "