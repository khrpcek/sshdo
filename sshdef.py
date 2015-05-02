#setup paramiko ssh info
import os
import paramiko
from colors import red, green
import time
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
datetime = time.strftime("%m%d%Y-%H%M%S")
#sftp = paramiko.SFTPClient()
#sftp.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#from demo.py. agent auth setup
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

def sshdo_questions():
    servers = raw_input('Servers: ')
    command = raw_input('Command: ')
    
    if len(servers.split()) > 1:
        list = servers.split()
    elif len(servers.split()) == 1:
        list = explode_list(servers)
    return list

def sshdo():
    servers = raw_input('Servers: ')
    command = raw_input('Command: ')
    if not os.path.exists('logs'+datetime): os.makedirs('logs/'+datetime)

    if len(servers.split()) > 1:
        list = servers.split()
    elif len(servers.split()) == 1:
        list = explode_list(servers)
    for host in list:
        try:
            ssh.connect(host, username='root', allow_agent=True, timeout=5)
        except Exception:
            print red(host + "\n Could not connect \n")
        else:
            log_f = open('logs/'+datetime+'/'+host+'.log', 'w')
            log_f.write(command+"/n/n")
            paramiko.util.log_to_file('logs/test.log')
            print green("\n" + host + "\n")
            stdin, stdout, stderr = ssh.exec_command(command)
            for data_line in stdout:
                print data_line.rstrip()
                log_f.write(data_line)
            log_f.close()
            ssh.close()
    return 

def sshput():
    print "sshput block"

    #prompt for info
    servers = raw_input('Servers: ')
    local_file = raw_input('Local File or Direcotry: ')
    remote_dir = raw_input('Remote Location: ')
    remote_base_file = os.path.basename(local_file)
    remote_file = remote_dir + remote_base_file

    if len(servers.split()) > 1:
        list = servers.split()
    elif len(servers.split()) == 1:
        list = explode_list(servers)

    for host in list:
        try:
            ssh.connect(host, username='root', allow_agent=True, timeout=5)
        except Exception:
            print red(host + "\n Could not connect \n")
        else:
            print green("\n" + host + "\n")
            sftp = ssh.open_sftp()
            sftp.put(local_file,remote_file,confirm=True)
            ssh.close()
        
    return "sshput"
def sshget():

    #prompt for info
    servers = raw_input('Servers: ')
    remote_file = raw_input('Remote File: ')
    local_dir = raw_input('Local Drop Directory: ')
    remote_base_file = os.path.basename(remote_file)

    if len(servers.split()) > 1:
        list = servers.split()
    elif len(servers.split()) == 1:
        list = explode_list(servers)

    for host in list:
        try:
            ssh.connect(host, username='root', allow_agent=True, timeout=5)
        except Exception:
            print red(host + "\n Could not connect \n")
        else:
            print green("\n" + host + "\n")
            local_file = local_dir + host + "." + remote_base_file
            sftp = ssh.open_sftp()
            sftp.get(remote_file,local_file)
            ssh.close()
    return "sshget"


