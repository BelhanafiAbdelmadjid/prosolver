from main import app   , db , ExpectedServersUAT , ExpectedServersPROD , DOMAIN
from main.Models import *
import paramiko
import random
from io import StringIO
import ping3
import time

def innitServerDictionarry():
    with app.app_context():
        servers = Servers.query.all()
        for server in servers :
            if server.type.value == "UAT" :
                ExpectedServersUAT[server.name] = server.ip
            else :
                ExpectedServersPROD[server.name] = server.ip

        
def initialisationConnexionRandom(username:str,password:str,dict:dict):
    print("choosing...")
    username = username.strip(" ")+DOMAIN
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    listSrv = list(dict.values())
    print(listSrv)
    randomIndex = 0
    if len(listSrv)> 1 :
        randomIndex = random.randrange(0,len(listSrv)-1)
    print("index",randomIndex)
    tryCoTo = listSrv[randomIndex].strip(" ")
    print(tryCoTo)
    client.connect(tryCoTo,username=username,password=password)
    print("Connected")
    client.close()

def isMyHostUp(srv):
    print("cheking",srv)
    response = ping3.ping(srv,timeout=4)
    if response :
        return True
    return False

def executeCommande(ip,username,password,cmd,expectedOutputNumber=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try :
        client.connect(ip,username=username,password=password)
    except paramiko.ssh_exception.NoValidConnectionsError :
        raise ValueError("SSH on server is not active.")
    finalCmd = "echo "+ password  +" | sudo -S "+ cmd 
    stdin, stdout, stderr = client.exec_command(finalCmd)
    stdin.flush()
    result = stdout.read().decode().split("\n")
    client.close()
    if(len(result)> 1):
        if result[-1] == "":
            result.pop()
        if not result[-1] == "0" and len(result) == 1:
            return []
    if expectedOutputNumber is not None :
        expectedOutputNumber = expectedOutputNumber + 1
        if(len(result) < expectedOutputNumber):
            result = result[len(result)-expectedOutputNumber:len(result)]
    client.close()
    print(result)
    return result
def executeScript(ip,username,password,script,header,arguments,expectedOutputNumber,onServer):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,username=username,password=password)
    script_io = StringIO(script)
    script_io.seek(0)
    
    if onServer == True :
        if arguments:
            arguments = " ".join("'"+arguments+"'")
            header = header+" "+arguments
        stdin, stdout, stderr =  client.exec_command(header)
        stdin.write(script_io.getvalue())
        stdin.flush()
    else :
        getContainerID =  f'echo \'{password}\' | sudo -S  docker ps -q -f name={header[0]}  '
        stdin, stdout, stderr =  client.exec_command(getContainerID)
        stdin.write(script_io.getvalue())
        stdin.flush()
        while stdout.channel.exit_status_ready()!= True or stderr.channel.exit_status_ready() != True :
            pass     

        containerID = stdout.read().decode()   
        error = stderr.read().decode()
        print("GET CONTAINER ID RESULT")
        print("error",error)
        print("result",containerID)
        if not containerID :
            return None , error   
        # ScriptContent = script_io.getvalue().replace("\n"," ")
        ScriptContent = script_io.getvalue()
        header = "echo '" + password + "' | sudo -S docker exec -i " + containerID.strip("\n") + ' ' + header[1] + ' "' + ScriptContent + '" '
        print(arguments)
        if arguments:
            arguments = [str(argument) for argument in arguments]
            arguments = " ".join(arguments)
            header = header+" "+arguments
        print(header)
        stdin, stdout, stderr =  client.exec_command(header)
    
    stdin.channel.shutdown_write()
    while stdout.channel.exit_status_ready()!= True or stderr.channel.exit_status_ready() != True :
        pass

    result = stdout.readlines()

    print("result",result)

    result = result[len(result)-expectedOutputNumber:]
    result = "\n".join(result)
    error = stderr.read().decode()

    client.close()

    print("error",error)
    print("result",result)
    
    return result,error  
