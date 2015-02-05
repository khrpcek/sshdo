#!/usr/bin/python

#sshdo, get, cp, all compiled into one script
#add in logging capabilities
#use list files in a subdirectory for sources
#but have it just read in ./sshdo.py asdf and it reads asdf.txt
# run as ./sshdo list cp,get

import sys
import subprocess
import paramiko
import base64
from sshdef import *

if len(sys.argv) > 1:

    if sys.argv[1] == "get":
        #block for getting a file from all servers
#        serv_list = questions()
        sshget()
    elif sys.argv[1] == "put":
        #block for putting a file
#        serv_list = questions()
        sshput()
    elif sys.argv[1] == "help":
        #block for help text
        print "help info for n00bz"
elif len(sys.argv) == 1:
    #run sshdo
#    print sshdo_questions()
    print sshdo()

