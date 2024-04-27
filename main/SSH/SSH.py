from .. import app
from paramiko import SSHClient,AutoAddPolicy,ssh_exception
import ping3

def initClient():
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    return client

class ServerToolKit():
    def __init__(self,server_ip,server_name=None):
        self.client = initClient()
        self.server_name = server_name 
        self.server_ip = server_ip
    def __str__(self) -> str:
        return f'SSHCLIENT for {self.server}'
    
    # ---------------------------------------------------------------------------- #
    #                              functional commands                             #
    # ---------------------------------------------------------------------------- #
    def execute(self,cmd,write=None) -> list  :
        try :
            self.client.connect(
                self.server_ip,
                username=app.config.get("USER_APP"),
                password=app.config.get("USER_APP_PASSWORD")
                )
        except ssh_exception.AuthenticationException as e :
            raise ValueError("Authentification using user app failed.")
        except ssh_exception.NoValidConnectionsError :
            raise ValueError("SSH on server not active.")
        
        cmd = f'sudo {cmd}'
        print("FINALE COMMAND",cmd)
        stdin, stdout, stderr = self.client.exec_command(cmd)

        if write is not None :
            stdin.write(write)
            stdin.flush()
            stdin.channel.shutdown_write()
            while stdout.channel.exit_status_ready()!= True or stderr.channel.exit_status_ready() != True :
                pass

        result = stdout.readlines()
        error = stderr.readlines()
        
        self.client.close()
        return result , error
    
    def isMyHostUp(self) -> bool:
        response = ping3.ping(self.server_ip,timeout=4)
        if response :
            return True
        return False

    

class ContainerToolKit(ServerToolKit):
    def __init__(self, server_ip, container_name, container_ID =None , server_name=None):
        self.container_name = container_name
        self.container_ID = container_ID
        super().__init__(server_ip, server_name)

    def getContainerID(self) -> str:
        result , error = self.execute(f'docker ps -q -f name={self.container_name}')
        if len(result)<=0 :
            raise ValueError("Cannot get container ID.")
        '''
            receiving result as follow: ["7D8SQ9D\n"]
        '''
        result = result[0].strip("\n")
        self.container_ID = result
        return result