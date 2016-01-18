#!/usr/bin/python

#sshdo, get, cp, all compiled into one script
#use list files in a subdirectory for sources
#but have it just read in ./sshdo.py asdf and it reads asdf.txt
# run as ./sshdo list cp,get

import sys, os, time, argparse
import paramiko, tarfile, shutil
from colors import red, green

def agent_auth(transport, username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent.
    """
    agent = paramiko.Agent()
    agent_keys = agent.get_keys()
    if len(agent_keys) == 0:
        return
    for key in agent_keys:
        print('Trying ssh-agent key %s' % hexlify(key.get_fingerprint()))
        try:
            transport.auth_publickey(username, key)
            print('... success!')
            return
        except paramiko.SSHException:
            print('... nope.')

def explode_list(list_name):
    file_name = 'lists/' + list_name
    servers_file = open(file_name, 'r')
    servers_list = servers_file.readlines()
    servers_list_stripped = [line.rstrip() for line in servers_list]
    servers_file.close()
    return servers_list_stripped

def server_list(server_input):
    if len(server_input.split()) > 1:
        list = server_input.split()
    elif len(server_input.split()) == 1:
        list = explode_list(server_input)
    return list

def sshdo(args, sshdo_dir):
    servers = raw_input('Servers: ')
    command = raw_input('Command: ')
    #if not os.path.exists('logs'+datetime): os.makedirs('logs/'+datetime)
    if not os.path.exists("{0}/logs/{1}".format(sshdo_dir, log_dir)): os.makedirs("{0}/logs/{1}".format(sshdo_dir, log_dir))

    list = server_list(servers)

    fail_to_connect = []
    for host in list:
        try:
            ssh.connect(host, username='root', allow_agent=True, timeout=5)
        except Exception:
            print red(host + "\n Could not connect \n")
            fail_to_connect.append(host)
        else:
#            log_f = open('logs/'+datetime+'/'+host+'.log', 'w')
            log_f = open("{0}/logs/{1}/{2}.log".format(sshdo_dir, log_dir, host), 'w')
            log_f.write(command+"/n/n")
            if args.debug:
                paramiko.util.log_to_file("{0}/logs/debug.log".format(sshdo_dir))
            print green("\n" + host + "\n")
            stdin, stdout, stderr = ssh.exec_command(command)
            for data_line in stdout:
                print data_line.rstrip()
                log_f.write(data_line)
            log_f.close()
            ssh.close()
    if len(fail_to_connect) > 0:
        print red("Failed to connect to these hosts %s" % (fail_to_connect))
    print "Log files are in logs/%s" % (log_dir)
    return

def sshput():
    print "sshput block"

    #prompt for info
    servers = raw_input('Servers: ')
    local_file = raw_input('Local File or Direcotry: ')
    remote_dir = raw_input('Remote Location: ')
    remote_base_file = os.path.basename(local_file)
    remote_file = remote_dir + remote_base_file

    list = server_list(servers)

    fail_to_connect = []
    for host in list:
        try:
            ssh.connect(host, username='root', allow_agent=True, timeout=5)
        except Exception:
            print red(host + "\n Could not connect \n")
            fail_to_connect.append(host)
        else:
            print green("\n" + host + "\n")
            sftp = ssh.open_sftp()
            sftp.put(local_file,remote_file,confirm=True)
            ssh.close()
    if len(fail_to_connect) > 0:
        print red("Failed to connect to these hosts %s" % (fail_to_connect))
    return "sshput"

def sshget():

    #prompt for info
    servers = raw_input('Servers: ')
    remote_file = raw_input('Remote File: ')
    local_dir = raw_input('Local Drop Directory: ')
    remote_base_file = os.path.basename(remote_file)

    list = server_list(servers)

    fail_to_connect = []
    for host in list:
        try:
            ssh.connect(host, username='root', allow_agent=True, timeout=5)
        except Exception:
            print red(host + "\n Could not connect \n")
            fail_to_connect.append(host)
        else:
            print green("\n" + host + "\n")
            local_file = local_dir + host + "." + remote_base_file
            sftp = ssh.open_sftp()
            sftp.get(remote_file,local_file)
            ssh.close()
    if len(fail_to_connect) > 0:
        print red("Failed to connect to these hosts %s" % (fail_to_connect))
    return "sshget"
def logtar(sshdo_dir):
#keep these many dirs untar'd
    untar=4
    logs_list = os.listdir('%s/logs' % (sshdo_dir))
    tars = [s for s in logs_list if "tar.gz" in s]
    for i in tars:
        logs_list.remove(i)
    if '.gitignore' in logs_list:
        logs_list.remove('.gitignore')
    if 'debug.log' in logs_list:
        logs_list.remove('debug.log')
#at this point logs_list has excluded .gitignore and all tar.gz files
    if (len(logs_list) == 0) or (len(logs_list) <= untar):
        exit()
    elif len(logs_list) > untar:
        #datetime_files = [datetime.strptime(a, "%m%d%Y-%H%M%S") for a in logs_list]
        #sorted_list = [datetime.strftime(a, "%m%d%Y-%H%M%S") for a in datetime_files]
        sorted_list = sorted(logs_list)
        sorted_list = sorted_list[:len(sorted_list)-untar]
        for i in sorted_list:
            tar = tarfile.open("%s/logs/%s.tar.gz" % (sshdo_dir, i), "w:gz")
            tar.add("%s/logs/%s" % (sshdo_dir, i), arcname=i)
            tar.close()
            shutil.rmtree("%s/logs/%s" % (sshdo_dir, i))
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a command or sftp on many servers. Only sshdo operations are logged, put and get are not logged since there is generally no output. Running without put or get allows for ssh operation.')
    parser.add_argument('--put',help='Use sftp to put files')
    parser.add_argument('--get',help='Use sftp to get files. Files are prefixed with the hostname they are from.')
    #not built in yet, next version perhaps parser.add_argument('--nolog', help='Disables logging')
    parser.add_argument('--debug', help='Enables paramiko debug logging. Goes to logs/debug.log',action='store_true')
    args = parser.parse_args()
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    log_dir = time.strftime("%m%d%Y-%H%M%S")
    sshdo_dir = os.path.dirname(os.path.realpath(__file__))
    
    if args.put:
        sshput()
    elif args.get:
        sshget()
    else:
        sshdo(args, sshdo_dir)
        logtar(sshdo_dir)
