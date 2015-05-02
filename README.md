##sshdo.py

khrpcek@gmail.com

This is a small script for doing mass SSH operations on servers. There are currently three components to it, sshdo, put, and get. The servers are located in files in the lists subdirectory. If you enter a list name when it prompts for servers it will use all hosts listed in that file. The files should be 1 host per line. You can also maually type in the hosts at the Servers prompt (space delimited).

###Dependencies:
* Paramiko
* Ansicolors

Use pip to install these or do it manually.

###sshdo
Usage: ./sshdo.py
Executes the given command on all hosts in the list or typed in.

###put
Usage: ./sshdo.py put
This sftp's the given file to the given location on all remote hosts in the list or typed in manually.

###get
Usage: ./sshdo get
SFTPs the given file from each server to the given location on the host you are running sshdo on. It will prefix the file name with the host/ip you connected to the remote host with.

###TODO
* More exception handling
* Option to disable logging
* Log Compression
* Log rotation
* Threading option
* Failed list at end instead of in standard out
