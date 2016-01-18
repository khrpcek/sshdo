##sshdo.py

khrpcek@gmail.com

This is a small script for doing mass SSH operations on servers. There are currently three components to it, sshdo, put, and get. The servers are located in files in the lists subdirectory. If you enter a list name when it prompts for servers it will use all hosts listed in that file. The files should be 1 host per line. You can also maually type in the hosts at the Servers prompt (space delimited).

###Dependencies:
* Paramiko
* Ansicolors

Use pip to install these or do it manually.

###Usage
usage: sshdov2.py [-h] [--put PUT] [--get GET] [--debug]

Run a command or sftp on many servers. Only sshdo operations are logged, put
and get are not logged since there is generally no output. Running without put
or get allows for ssh operation.

optional arguments:
  -h, --help  show this help message and exit
  --put PUT   Use sftp to put files
  --get GET   Use sftp to get files. Files are prefixed with the hostname they
              are from.
  --debug     Enables paramiko debug logging. Goes to logs/debug.log


###sshdo
Usage: ./sshdo.py
Executes the given command on all hosts in the list or typed in.

###put
Usage: ./sshdo.py --put
This sftp's the given file to the given location on all remote hosts in the list or typed in manually.

###get
Usage: ./sshdo --get
SFTPs the given file from each server to the given location on the host you are running sshdo on. It will prefix the file name with the host/ip you connected to the remote host with.

###Changelog
* 1/18/2016
 * Cleaned up code. Reduced all code to 1 file. 
 * Removed base64 module
 * It now requires shutil, argparse, and tarfile modules
 * Fixed Logging
 * Added log compression. It tar/gzips the log folders older than 4 operations. You can change this value by setting the untar variable in the script.
 * Prints list at end of script for failed hosts
 * Prints log directory for current operation at end of script
 * Now uses full paths for files so that you can execute sshdo from outside it's own directory


###TODO
* More exception handling
* Option to disable logging
* Threading option
