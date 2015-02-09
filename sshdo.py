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
        sshget()
    elif sys.argv[1] == "put":
        sshput()
    elif sys.argv[1] == "help":
        print "help info for n00bz"
elif len(sys.argv) == 1:
    #run sshdo
#    print sshdo_questions()
    print sshdo()

