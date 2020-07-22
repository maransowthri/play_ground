import subprocess
import logging
import paramiko

p1 = subprocess.run(['python', '--version'], shell=True, capture_output=True, text=True)
print(type(p1.stdout))
print(p1.stdout)

# server = '172.17.0.3'
# username = 'root'
# password = 'pass123'
# cmd_to_execute = 'python --version'

# ssh = paramiko.SSHClient()

# ssh.connect(server, username=username, password=password)
# ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)