# -*- coding: utf-8 -*-
import imp
import glob
import multiprocessing
import Queue
import threading
import configparser
import os
import sys
import warnings
import time
import subprocess
from Common import Helpers


class Conducter:

  def __init__(self):
    self.RecpEmails = []
    self.SendersEmail = ''
    self.SendersPass = ''
    self.modules = {}
    self.dmodules = {}
    self.load_modules()

  def load_modules(self):
    # loop and assign key and name
    warnings.filterwarnings('ignore', '.*Parent module*',)
    x = 1
    for name in glob.glob('Modules/*.py'):
        if name.endswith(".py") and ("__init__" not in name):
            loaded_modules = imp.load_source(
                name.replace("/", ".").rstrip('.py'), name)
            self.modules[name] = loaded_modules
            self.dmodules[x] = loaded_modules
            x += 1
    return self.dmodules
    return self.modules

  def ListModules(self):
      print Helpers.color(" [*] Available Modules are:\n", blue=True)
      lastBase = None
      x = 1
      for name in self.modules:
          parts = name.split("/")
          if lastBase and parts[0] != lastBase:
              print ""
          lastBase = parts[0]
          print "\t%s)\t%s" % (x, '{0: <24}'.format(name))
          x += 1
      print ""
 
  #def ExecuteModule(self, sleep_time, max_sms, senders_email, senders_password, iptables_log):
