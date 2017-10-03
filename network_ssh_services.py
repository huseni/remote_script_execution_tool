#!/usr/bin/env python
#######################################################################################################################
#                                                                                                                     #
# THIS SCRIPT IS TO OPEN A SOCKET OVER A TCP LAYER WITH MULTIPLE CLIENTS, TRANFER FILES AND RUN VARIOUS COMMANDS NOT  #
# LIMITED TO PERFORM SPECIFIC TASK BUT INCLUDING INSTALLING OS PACKAGE, FILE PERMISSIONS, SYSTEM CONFIG, ETC          #
# VERSION 1.0                                                                                                         #
# USAGE:                                                                                                              # 
#       python network_ssh_services.py                                                                                #
#                                                                                                                     #
#######################################################################################################################
import paramiko
import os


class networkAPI(object):
    """
    Functionality to copy the files over the remote machines and proceeds with installing software
    """
    def __init__(self, host, port=22, user='ubuntu', host_private_key_file, file_list, file_path, run_cmd, run_cmd_path):
        """
        To initialize the paramico connection over the socket to the remote client machine to perfrom network operations
        """
        self.file_list = file_list
        self.file_path = file_path
        self.run_cmd = run_cmd
        self.run_cmd_path = run_cmd_path

        paramiko.util.log_to_file('paramico.log')
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey.from_private_key_file(host_private_key_file)
        
        print("****************** Establishing the connection with the remote servers.....*************************")
        self.ssh.connect(host, port=port, username=user, pkey=private_key, timeout=3.0)
        self.sftp = self.ssh.open_sftp()

    
    def copy_files(self):
        """
        To copy the file on remote machine on the specified location
        """ 
        print("************* Initializing the secure FTP connection over the network ....*********************") 
        for fil in self.file_list:
            self.sftp.put(fil, os.path.join(self.file_path, fil))

    
    def execute_remote_script(self):
        """
        To execute the script on the remote server through the secure paramico object socket
        """
        print("***************** Execute remote commands *******************")
        cmd = os.path.join(self.run_cmd_path,self.run_cmd)
        self.sftp.chdir(self.run_cmd_path) 
        self.sftp.chmod(cmd, 0755)
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        print "stderr: ", stderr.readlines()
        print "pwd: ", stdout.readlines()   
   

    def __del__(self):
        """
        To close the secure paramico connection to the remote machine over the socket
        """
        self.sftp.close() 
        self.ssh.close()       


# Main function execution with required parameters#
def main():
    host_private_key_file = '/home/ubuntu/mykey.pem'
    file_list = ['filebeat.yml','install_filebeat_client.sh']
    file_path = '/home/ubuntu' 
    run_cmd = 'install_filebeat_client.sh'
    run_cmd_path = '/home/ubuntu' 
    port = 22
    user = 'ubuntu'
    host_list = ['46.3.41.4', '88.16.95.10']
    for host in host_list:
        p = networkAPI(host, port, user, host_private_key_file, file_list, file_path, run_cmd, run_cmd_path)
        p.copy_files()
        p.execute_remote_script()


# Main execution point
if __name__ == '__main__':
    main()
