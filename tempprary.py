from paramiko import SSHClient,AutoAddPolicy,ssh_exception
import os

os.environ["USER_APP_SSH"] = 'userapp' 
os.environ["USER_APP_SSH_PASSWORD"] = 'userapp' 



def executeCommande(ip,username,password,cmd,expectedOutputNumber=None):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(ip,username=username,password=password)
    finalCmd = " sudo "+ cmd 
    print(finalCmd)
    stdin, stdout, stderr = client.exec_command(finalCmd)
    stdin.flush()
    result = stdout.readlines()
    error = stderr.readlines()
    client.close()
    return result,error
print("HERE ARE VAR ENV",os.environ.get("USER_APP_SSH"),os.environ.get("USER_APP_SSH_PASSWORD"))
print(executeCommande(ip="192.168.1.66",
                      username=os.environ.get("USER_APP_SSH_PASSWORD")
                      ,password=os.environ.get('USER_APP_SSH_PASSWORD'),
                      cmd='docker ps -a',
                      expectedOutputNumber=9999))