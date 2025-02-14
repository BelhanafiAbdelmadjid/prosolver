from datetime import datetime
from main import db
from sqlalchemy import CheckConstraint , event
import ipaddress
import enum
import ping3
import paramiko
from io import StringIO

from .SSH.SSH import ServerToolKit,ContainerToolKit

def executeScript(ip,username,password,script,header,arguments,expectedOutputNumber,onServer):

    script_io = StringIO(script)
    script_io.seek(0)
    
    if onServer == True :

        toolKit = ServerToolKit(server_ip=ip)
        
        if arguments:
            arguments = " ".join("'" + str(arg) + "'" for arg in arguments)
            header = header+" "+arguments
        result , error = toolKit.execute(header,write=script_io.getvalue())
    else :
        toolKit = ContainerToolKit(server_ip=ip,container_name=header[0])
        toolKit.getContainerID()
        
        ScriptContent = script_io.getvalue()
        
        header = "docker exec -i " + toolKit.container_ID + ' ' + header[1] + ' "' + ScriptContent + '" '
        
        if arguments:
            arguments = " ".join("'" + str(arg) + "'" for arg in arguments)
            header = header+" "+arguments

        result , error = toolKit.execute(header)

    return result,error  


class ServersType(enum.Enum):
    UAT = 'UAT'
    PROD = "PROD"
class ServersTypeOS(enum.Enum):
    Linux = 'Linux'
    Windows = "Windows"    
class InputType(enum.Enum):
    EMAIL = "email"
    TEXT = "text"
    PHONE_NUMBER = "tel"
    CHECK_BOX = "checkbox"
    DATE = "date"
    NUMBER = "number"
class languages(enum.Enum):
    RUBY = "ruby"
    PYTHON = "python"
    BASH = "bash"
def attributeInEnum(attribute,EnumClass):
    return attribute in [member.value for member in EnumClass]


class Servers(db.Model):
    # -------------------------------- Primary key ------------------------------- #
    id = db.Column(db.Integer,primary_key = True)
    # -------------------------------- Attributes -------------------------------- #
    ip = db.Column(db.String(15),nullable=False,unique=True)
    name = db.Column(db.String(50),nullable=False,unique=True)
    type = db.Column(db.Enum(ServersType),nullable=False)
    type_os = db.Column(db.Enum(ServersTypeOS),nullable=False)
    # ------------------------------- Foreing keys ------------------------------- #
    addedBy = db.Column(db.Integer, db.ForeignKey('users.id'))
    # ---------------------------- Giving foreing keys --------------------------- #
    containers = db.relationship("Containers",backref="server_relation",cascade="all,delete")
    steps = db.relationship("Steps",backref="server_relation")
    # ------------------------------ Static methods ------------------------------ #
    @staticmethod
    def create(name,type,ip,addedBy,containers,type_os):
        if Servers().getServerByIP(ip):
            raise ValueError(f'Server with ip: {ip} already exist.')
        if Servers().checkIfNameExist(name) :
            raise  ValueError(f'Server name {name} already exists.')
        if len(name) <= 0 :
            raise ValueError(f'Server name cannot be empty.')
        server = Servers(name=name,ip=ip)
        # ------------------------------ handeling user ------------------------------ #
        if isinstance(addedBy,Users) :
            server.addedBy = addedBy.id
        elif Users().getUserByID(addedBy):
            server.addedBy = addedBy
        else:
            raise ValueError("User does not exist.")
        db.session.add(server)
        # ------------------------------ handeling type ------------------------------ #
        if attributeInEnum(type,ServersType):
            server.type = type
        else:
            raise ValueError(f'Type {type} is not supported please contact your support.')
        # ------------------------------ handeling type os ------------------------------ #
        if attributeInEnum(type_os,ServersTypeOS):
            server.type_os = type_os
        else:
            raise ValueError(f'Type of os {type_os} is not supported please contact your support.')
        # ---------------------------- handeling container --------------------------- #
        for container in containers :
            server.containers.append(Containers(name=container["name"],addedby=addedBy))
        db.session.add(server)
        return server
    @staticmethod
    def validate_ipv4(target, value, oldvalue, initiator):
        try:
            ipaddress.IPv4Address(value)
        except ipaddress.AddressValueError:
            raise ValueError("Invalid IPv4 address")
    @staticmethod
    def getServerByID(id):
        return Servers().query.filter_by(id=id).first()
    @staticmethod
    def getServerByIP(ip):
        return Servers().query.filter_by(ip=ip).first()
    @staticmethod
    def toStringServers(servers):
        res = []
        for server in servers :
            res.append(server.toString())
        return res
    @staticmethod
    def listAll(containers=False,ping=False,name=True,type=True,addedBy=True,ip=True,query_name=None):
        servers = Servers().query
        if query_name is not None :
            servers = servers.filter(Servers.name.ilike(f'%{query_name}%'))
        else :
            servers = servers.all()
        return [server.toDictionary(containers=containers,ping=ping,name=name,type=type,addedBy=addedBy,ip=ip) for server in servers]
    @staticmethod
    def checkIfNameExist(name,server=None):
        if server:
            potential = Servers().query.filter_by(name=name).first()
            return None if server == potential.id else property
        return Servers().query.filter_by(name=name).first()
    @staticmethod
    def listUATServers():
        return Servers().query.filter_by(type="UAT")
    @staticmethod
    def listProdServers():
        return Servers().query.filter_by(type="PROD")
    @staticmethod
    def listUATServersSupervision(query_name=None):
        servers = Servers().query
        if query_name is not None :
            servers = servers.filter_by(type="UAT").filter(Servers.name.ilike(f'%{query_name}%'))
        else :
            servers = servers.filter_by(type="UAT")
        servers = [server.toDictionary(containers=False,type=False,ping=True,addedBy=False) for server in servers]
        return servers
    @staticmethod
    def listProdServersSupervision(query_name=None):
        servers = Servers().query
        if query_name is not None :
            servers = servers.filter_by(type="PROD").filter(Servers.name.ilike(f'%{query_name}%'))
        else :
            servers = servers.filter_by(type="PROD")
        servers = [server.toDictionary(containers=False,ping=True,type_os=True) for server in servers]
        return servers
    # ---------------------------------- Methods --------------------------------- #
    def toDictionary(self,name=True,type=True,addedBy=True,ip=True,containers=False,ping=False,type_os=False):
        return  {
            "id" : self.id,
            "ip" : self.ip if ip else None,
            "name" : self.name if name else None,
            "type" : self.type.value if type else None,
            "type_os" : self.type_os.value if type_os else None,
            "addedBy" : Users().getUserByID(self.addedBy).user if addedBy else None,
            "containers" : Containers().listContainers(self.containers) if containers else [container.id for container in self.containers],
            "status" : ( self.hostIsUp() ) if ping else None 
        }
    def delete(self):
        if self.steps:
            raise ValueError("This server cannot be deleted since it is still implicated on currently used steps.")
        # ---------------------------------------------------------------------------- #
        #         containers will be deleted automatically cascade="all,delete"        #
        # ---------------------------------------------------------------------------- #
        db.session.delete(self)
    def hostIsUp(self):
        return "Active" if ping3.ping(self.ip,timeout=4) else "Down"
    def update(self,name,ip,type,containers,addedBy,type_os):
        if name :
            if Servers().checkIfNameExist(name):
                raise ValueError(f'Server with the name: {name} already exist.')
            self.name = name
        if ip:
            if Servers().getServerByIP(ip):
                raise ValueError(f'Server with the ip {ip} already exists.')
            self.ip = ip
        if type :
            if attributeInEnum(type,ServersType):
                self.type = type
            else:
                raise ValueError(f'Type {type} is not supported please contact your support.')
        if type_os :
            if attributeInEnum(type_os,ServersTypeOS):
                self.type_os = type_os
            else:
                raise ValueError(f'Type of os {type_os} is not supported please contact your support.')
        print("check containers",containers)
        if containers:
            oldContainers = [item for item in self.containers if item.id not in [x["id"] for x in containers]]
            newContainers = list(filter(lambda x: x['id'] is  None, containers))
            for container in oldContainers :
                container.delete()
            for container in newContainers: 
                c = Containers().create(name=container["name"],server = self.id,addedBy=addedBy)
                print("Container added",c.addedby)

event.listen(Servers.ip, 'set', Servers.validate_ipv4)

class Containers(db.Model):
    # -------------------------------- Primary key ------------------------------- #
    id = db.Column(db.Integer,primary_key = True)
    # -------------------------------- Attributes -------------------------------- #
    name = db.Column(db.String(50),nullable=False)
    # ------------------------------- Foreing keys ------------------------------- #
    server = db.Column(db.Integer,db.ForeignKey("servers.id"))
    addedby = db.Column(db.Integer,db.ForeignKey("users.id"))
    # ---------------------------- Giving foreing keys --------------------------- #
    steps = db.relationship("Steps",backref="containers_relation",lazy=True)
    # ------------------------------ Static methods ------------------------------ #
    @staticmethod
    def getContainerByID(id):
        return Containers().query.filter_by(id=id).first()
    @staticmethod
    def getContainersOfServer(id):
        return Containers().query.filter_by(server=id).all()
    @staticmethod
    def listContainers(containers):
        if all(isinstance(container,Containers) for container in containers):
            return [container.toDictionary() for container in containers]
        else :
            return [Containers().getContainerByID(container).toDictionary() for container in containers]
    @staticmethod
    def listAll():
        return [container.toDictionary() for container in Containers().query.all()]
    @staticmethod
    def checkIfContainerNameExistForServer(name,server):
        return Containers().query.filter_by(name=name,server=server).first()
    @staticmethod
    def create(name,server,addedBy):
        container = Containers()
        # ----------------------------- handeling server ----------------------------- #
        if Servers().getServerByID(server):
            container.server = server
        else:
            raise ValueError("Server does not exist.")
        # ------------------------- handeling container name ------------------------- #
        if Containers().checkIfContainerNameExistForServer(name,container.server):
            raise ValueError(f'Container {name} already exist this server.')
        container.name = name
        # ------------------------------ handeling user ------------------------------ #
        if Users().getUserByID(addedBy):
            container.addedby = addedBy
        else:
            raise ValueError("User does not exist.")
        db.session.add(container)
        return container
    @staticmethod
    def deleteWithID(id):
        container = Containers().getContainerByID(id)
        if not container :
            raise ValueError("Container does not exist.")
        container.delete()
    @staticmethod
    def containerBelongToServer(server,container):
        return Containers().query.filter_by(server=server,id=container).first()
    # ---------------------------------- Methods --------------------------------- #
    def delete(self):
        if self.steps :
            raise ValueError("Cannot delete this container, it is still used in a step.")
        db.session.delete(self)
    def toDictionary(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "addedBy" : Users().getUserByID(self.addedby).user
        }
    def update(self,name):
        if Containers().checkIfContainerNameExistForServer(name,self.server) :
            raise ValueError(f'Container {name} already exist this server.')
        self.name = name

class Steps(db.Model):
    # ------------------------------- Primary keys ------------------------------- #
    id = db.Column(db.Integer,primary_key = True)
    # -------------------------------- Attributes: ------------------------------- #
    name = db.Column(db.String(45), nullable=False)
    order = db.Column(db.Integer,nullable = False)
    onServer = db.Column(db.Boolean,nullable=False)
    # ------------------------------- Foreing keys ------------------------------- #
    incidentID = db.Column(db.Integer,db.ForeignKey("incidents.id"))
    scriptID = db.Column(db.Integer, db.ForeignKey('scripts.id', ondelete='RESTRICT'))
    commandID = db.Column(db.Integer,db.ForeignKey("commands.id"))
    server = db.Column(db.Integer,db.ForeignKey("servers.id"))
    container = db.Column(db.Integer,db.ForeignKey("containers.id"))
    addedBy = db.Column(db.Integer,db.ForeignKey("users.id"))
    # ---------------------------- Giving foreing keys --------------------------- #
    inputs = db.relationship("InputsInStep",backref="steps_relation",cascade="all,delete",order_by='InputsInStep.order',lazy=True)
    # ------------------------------ Static methods ------------------------------ #
    @staticmethod
    def stepUsingScript(id):
        return Steps().query.filter_by(scriptID=id).all()
    @staticmethod
    def getStepByID(id):
        return Steps().query.filter_by(id=id).first()
    @staticmethod
    def listAll():
        steps = Steps().query.all()
        return[step.toDictionary() for step in steps]
    @staticmethod
    def  stepNameForIncidentExists(incident,name):
        return Steps().query.filter_by(name=name,incidentID=incident).first()
    @staticmethod
    def create(name,onServer,incident,script,server,container,inputs,addedBy):
        # ---------------------------- handeling incident ---------------------------- #

        incident = Incidents().getIncidentByID(incident)
        if not incident :
            raise ValueError("Incident does not exist.")
        # ---------------------------- handeling step name --------------------------- #
        if name is None or len(name) <= 0 :
            raise ValueError("Step name cannot be empty ")
        if Steps().stepNameForIncidentExists(incident.id,name):
            raise ValueError(f'Step with the name {name} already exists for this incident.')
        
        step = Steps(name=name,order=len(incident.steps),onServer=onServer,incidentID=incident.id)
        # ----------------------------- handeling script ----------------------------- #
        if script is None :
            raise ValueError("Script name cannot be empty ")
        script = Scripts().getScriptByID(script)
        if not script:
            raise ValueError("Script does not exist.")
        step.scriptID = script.id
        # ----------------------------- handeling command ---------------------------- #
        command = Commands().selectCommand(step.onServer,script.language)
        if not command:
            raise ValueError(f'Please add a command for this {script.language},server and containers combination.')
        step.commandID = command.id
        # ----------------------------- handeling server ----------------------------- #
        if server is None :
            raise ValueError("Server name cannot be empty ")
        if not Servers().getServerByID(server) :
            raise ValueError("Server does not exist")
        step.server = server
        # --------------------------- handeling containers --------------------------- #
        if container :
            if not Containers().getContainerByID(container) :
                raise ValueError("Container does not exist")
            step.container = container
        # ------------------------------ handeling user ------------------------------ #
        if isinstance(addedBy,Users) :
            step.addedBy = addedBy.id
        elif Users().getUserByID(addedBy):
            step.addedBy = addedBy
        else:
            raise ValueError("Script does not exist.")
        # ----------------------------- handeling inputs ----------------------------- #
        db.session.add(step)
        db.session.commit()
        if inputs :
            try :
                with db.session.no_autoflush:
                    step.inputs = [InputsInStep().create(None,parentInput=input["parentInput"],order=index+1) for index,input in enumerate(inputs)]
                    if(len(step.inputs)) != len(script.inputs):
                        raise ValueError(f'{script.name} needs {len(script.inputs)} input and your have selected {len(step.inputs)} inputs.')
            except Exception as e  :
                print("roll back")
                db.session.rollback()
                raise ValueError(e)
        elif len(script.inputs) !=0 :
            raise ValueError(f'Script {script.name} needs {len(script.inputs)} input and your have selected {0} inputs.')

        return step
    @staticmethod
    def stepCreateVue(incident):
        res = {
            **incident.toDictionary(name=True,inputs=True,description=False,addedBy=False),
            **{"servers" : Servers().listAll(containers=True,ip=False,addedBy=False,type=True,ping=False) },
            **{"scripts" : Scripts().listAll(content=False,name=True,outPutLinesNumber=False,addedBy=False,description=False,params=False,language=True,inputs=False)},
            }  

        return res
    @staticmethod
    def joinInputsIncidentStep(incident,script):
        incidentInputs = incident.inputs
        scriptInputs = script.inputs
        res = []
        for  scriptInput in  scriptInputs:
            found = False
            for  incidentInput in  incidentInputs:
                if(incidentInput.label.lower() == scriptInput.label.lower() and incidentInput.type == scriptInput.type ):
                    found = True
                    scriptInputFixed = scriptInput.toDictionary()
                    scriptInputFixed["incidentID"] = incidentInput.id
                    scriptInputFixed["scriptID"] = scriptInput.id
                    del scriptInputFixed["id"]
                    scriptInputFixed["parentInput"] = None
                    scriptInputFixed["fromIncident"] = True
                    res.append(scriptInputFixed)
            if not found :
                temp = scriptInput.toDictionary()
                temp["parentInput"] = temp["id"]
                temp["fromIncident"] = False
                del temp["id"]
                res.append(temp)
                #inputs from incident not matchhing are getting ignored here
        return res
    # ---------------------------------- Methods --------------------------------- #
    def joinInputsOrGetOldOnes(self,incident,script):
        if self.scriptID == script.id and self.incidentID == incident.id:
            return [inputInStep.toDictionary() for inputInStep in self.inputs ]
        else :
            return Steps().joinInputsIncidentStep(incident=incident,script=script)
    def getStepInputs(self):
        return self.inputs
    def delete(self):
        db.session.delete(self)
    def toDictionary(self,NameOrder=None,server=None,script=None):
        if NameOrder is True:
            return {
                    "id" : self.id,
                    "order" : self.order,
                    "name" : self.name,
            }
        return {
            "id" : self.id,
            "order" : self.order,
            "name" : self.name,
            "onServer" : self.onServer,
            "incident" : self.incidentID,
            "script" : self.scriptID if script is None else (lambda scrpt: {"name" : scrpt.name,"id" : scrpt.id} )(Scripts().getScriptByID(self.scriptID)) ,
            "command": (lambda c: " ".join([c.keyWord , c.paramsKeyWord]) if c.paramsKeyWord else c.keyWord)(Commands().getCommandByID(self.commandID)),
            "server" : self.server if server is None else (lambda srv: {"name" : srv.name,'ip' : srv.ip,'id' : srv.id} )(Servers().getServerByID(self.server)),
            "container" : None if  self.onServer else ((lambda cnt: {"name" : cnt.name,"id": cnt.id  } if cnt else None )(Containers().getContainerByID(self.container)) )  ,
            "addedBy" : Users().getUserByID(self.addedBy).user,
            "inputs" : InputsInStep().listAllForStep(self.id)
        }
    def update(self,name=None,order=None,script=None,onServer=None,server=None,container=None,inputs=None,addedBy=None):
        #command should be handeleld automatically
        # ---------------------------- handeling step name --------------------------- #
        if name :
            if self.name != name and Steps().stepNameForIncidentExists(self.incidentID,name):
                raise ValueError(f'Step with the name {name} already exists for this incident.')
            self.name = name
        # ---------------------------- handeling script ----------------------------- #
        if script:
            script = Scripts().getScriptByID(script)
            if not script:
                raise ValueError("Script does not exist.")
            self.scriptID = script.id
            self.inputs = []
        if order:
            if order <= 0 :
                raise ValueError(f'Step order must be positive, not {order}.')
            self.order = order
        if onServer is not None:
            if onServer == False  :
                self.onServer = False
                if not container:
                    raise ValueError(f'You specified that this step concerns containers, but you haven\'t selected any.')
                elif container :
                    if server is not None and server != self.server :
                        print("server is not NONe",server)
                        server = Servers().getServerByID(server)
                        if not server:
                            raise ValueError("Server does not exist.")
                        container = Containers().containerBelongToServer(server.id,container)
                        if not container :
                            raise ValueError("Container does not exist or belong to the selected server")
                        self.container = container.id
                        self.server = server.id
                    if server is None:
                        container = Containers().containerBelongToServer(self.server,container)
                        if not container :
                            raise ValueError("Container does not exist or belong to the selected server")
                        self.container = container.id
            elif onServer == True:
                if server is not None and server != self.server :
                    server = Servers().getServerByID(server)
                    if not server:
                        raise ValueError('Server does not exist.')
                    print("here")
                    self.server = server.id  
                self.onServer = True     
                self.container = None
        if inputs :
            if script is None:
                
                # updatedInputs = [updatedInput for updatedInput in inputs if "id" in updatedInput and updatedInput["id"] in [x.id for x in self.inputs]]
                for inputUpdate in inputs :
                    print(inputUpdate)
                    inputInStep = InputsInStep().getInputByID(inputUpdate["id"])
                    if not inputInStep :
                        raise ValueError("Input in step does not exist.")
                    input = Inputs().getInputByID(inputUpdate["parentInput"])
                    if not input :
                        raise ValueError("input does not exist.")
                    print(input.toDictionary())
                    if input.incidentID is not None and inputUpdate["fromIncident"] is False:
                        newInput = Inputs().getParallelInputForScript(inputUpdate["label"],self.scriptID)
                        if not newInput:
                            raise ValueError(f'Could not find input with the label {input["label"]} in the concerned script.')
                        inputInStep.parentInput = newInput.id
                    elif input.scriptID is not None and inputUpdate["fromIncident"] is True :
                        newInput = Inputs().getParallelInputForIncident(inputUpdate["label"],self.incidentID)
                        if not newInput:
                            raise ValueError(f'Could not find input with the label {inputUpdate["label"]} in the concerned incident.')
                        inputInStep.parentInput = newInput.id

            else :
                print("looking for new inputs")
                newInputs = list(filter(lambda x: 'id' not in x, inputs))

                for input in newInputs: 
                    try :
                        with db.session.no_autoflush:
                            print("Adding",input)
                            if "parentInput" in input and input["parentInput"] is None :
                                if input["fromIncident"] is True :
                                    input["parentInput"] = input["incidentID"]
                                else :
                                    input["parentInput"] = input["scriptID"]
                                del input["incidentID"]
                                del input["scriptID"]
                            self.inputs = [InputsInStep().create(self.id,parentInput=input["parentInput"],order=index+1) for index,input in enumerate(inputs)]
                            if(len(self.inputs)) != len(script.inputs):
                                raise ValueError(f'{script.name} needs {len(script.inputs)} input and your have selected {len(step.inputs)} inputs.')
                    except Exception as e  :
                        print("roll back")
                        db.session.rollback()
                        raise ValueError(e)
    def execute(self,userInputs,username,password):

        script = Scripts().getScriptByID(self.scriptID)
        command = Commands().getCommandByID(self.commandID)
        server = Servers().getServerByID(self.server)

        # --------------------------- handeling user inputs -------------------------- #
        finaleInputs = []
        try :
            print(userInputs)
            inputs = userInputs
            finaleInputs = []
            for input in inputs :
                if len(str(input["value"])) == 0:
                    raise ValueError(f'Inputs {input["label"]} cannot be empty.')
                finaleInputs.append(input["value"])
        except Exception as e:
            if len(userInputs) != 0 :
                raise ValueError(e)
            finaleInputs = None
        if finaleInputs != None and len(script.inputs) != len(finaleInputs) :
            raise ValueError(f'Please check your inputs, {script.name}-{script.language} needs {len(script.inputs)} inputs and you are passing {len(userInputs)}.')

        return self.executeOnServer(username=username,password=password,script=script,command=command,server=server,finaleInputs=finaleInputs) if self.onServer else self.executeOnContainer(username=username,password=password,script=script,command=command,server=server,finaleInputs=finaleInputs)
    def executeOnServer(self,script,command,server,finaleInputs,username,password):

        header = command.keyWord 

        if script.params :
            header = header + " " + command.paramsKeyWord
        return  executeScript(server.ip,username,password,script.content,header,finaleInputs,script.outPutLinesNumber,True)
    def executeOnContainer(self,script,command,server,finaleInputs,username,password):

        container = Containers().getContainerByID(self.container)
        header = command.keyWord 

        if script.params :
            header = header + " " + command.paramsKeyWord
        header =   [container.name,header]

        return  executeScript(server.ip,username,password,script.content,header,finaleInputs,script.outPutLinesNumber,False)

class Scripts(db.Model):
    # ------------------------------- Primary keys ------------------------------- #
    id = db.Column(db.Integer,primary_key = True)
    # -------------------------------- Attributes: ------------------------------- #
    name = db.Column(db.String(50),nullable=False)
    outPutLinesNumber = db.Column(db.Integer)
    description = db.Column(db.Text , nullable = False)
    content = db.Column(db.Text,nullable=False)
    params = db.Column(db.Boolean,nullable=False,default=False)
    # ------------------------------- Enum classes ------------------------------- #
    language = db.Column(db.Enum(languages),nullable = False)
    # ------------------------------- Foreing keys ------------------------------- #
    addedBy = db.Column(db.Integer,db.ForeignKey('users.id'))
    # ---------------------------- Giving foreing keys --------------------------- #
    steps = db.relationship("Steps", backref="script_relation",passive_deletes='all',lazy=True)
    inputs = db.relationship("Inputs",backref="script_relation",cascade="all,delete",lazy=True)
    # ------------------------------ Static methods ----------------------------- #
    @staticmethod
    def getScriptByName(name):
        return Scripts().query.filter_by(name=name).first()
    @staticmethod
    def getScriptByID(id):
        return Scripts().query.filter_by(id=id).first()
    @staticmethod
    def listAll(content=False,name=True,outPutLinesNumber=False,addedBy=False,description=True,params=False,language=True,inputs=False,query_name=None):
        scripts = Scripts().query
        if query_name is not None :
            scripts = scripts.filter(Scripts.name.ilike(f'%{query_name}%'))
        else :
            scripts = scripts.all()
        res = []
        for script in scripts :
            res.append(script.toDictionary(content=content,inputs=inputs,language=language,params=params,name=name,outPutLinesNumber=outPutLinesNumber,addedBy=addedBy,description=description))
        return res
    @staticmethod
    def create(name,outPutLinesNumber,description,content,params,language,inputs,addedBy):
        if name is None or len(name) == 0 :
            raise ValueError("Script name cannot be empty")
        script = Scripts(name=name,outPutLinesNumber=outPutLinesNumber,description=description,content=content,params=params)
        # ------------------------------ handeling user ------------------------------ #
        if isinstance(addedBy,Users) :
            script.addedBy = addedBy.id
        elif Users().getUserByID(addedBy):
            script.addedBy = addedBy
        else:
            raise ValueError("Script does not exist.")
        # ---------------------------- handeling language ---------------------------- #
        if language is None :
            raise ValueError('A language must be selected.')
        if attributeInEnum(language,languages):
            script.language = language
        else:
            raise ValueError(f'Language {language} is not supported please contact your support.')
        # ---------------------------------------------------------------------------- #
        #                                commiting here                                #
        # ---------------------------------------------------------------------------- #
        '''
            commiting here so script var can have an .id
        '''
        db.session.add(script)
        db.session.commit()
        for input in inputs :
            db.session.add(Inputs().create(label=input["label"],type=input["type"],scriptID=script.id,incidentID=None,addedBy=addedBy))
        return script
    # ---------------------------------- methods --------------------------------- #
    def delete(self):
        if Steps().stepUsingScript(self.id):
            raise ValueError("This script cannot be deleted since it is still implicated on currently used steps.")
        db.session.delete(self)
    def toDictionary(self,content=False,name=True,outPutLinesNumber=True,addedBy=True,description=True,params=True,language=True,inputs=True):
        '''
            if content is True, the content attribute will be returned
        '''
        res = {
            'id' : self.id,
            'name' : self.name if name else None,
            'outPutLinesNumber' : self.outPutLinesNumber if outPutLinesNumber else None ,
            'description' : self.description if description else None,
            'content' : self.content if content else None,
            'params' : self.params if params else None,
            'language' : self.language.value if language else None,
            'addedBy' : Users().getUserByID(self.addedBy).user if addedBy else None,
            'inputs' : [input.toDictionary() for input in self.inputs] if inputs else None
        }
        if content == True :
            res["content"] = self.content
        return res
    def update(self,name,outPutLinesNumber,description,content,params,language,inputs,addedBy):
        if name is not None :
            if Scripts().getScriptByName(name):
                raise ValueError(f'Script {name} already exists.')
            self.name = name
        if outPutLinesNumber is not None :
            if outPutLinesNumber < 0 :
                raise ValueError("Out put lines must be positive.")
            self.outPutLinesNumber = outPutLinesNumber
        if description is not None :
            self.description = description
        if content is not None :
            self.content = content
        if params is not None:
            self.params = params

        if language is not None :
            if attributeInEnum(language,languages):
                self.language = language
            else:
                raise ValueError(f'Language {language} is not supported please contact your support.')
        if inputs is not None : 
            print("****inputs before any modification****")
            for input in self.inputs:
                print(input)

            print("****All the inputs****")
            for input in inputs :
                print(input)

            oldInputs = [item for item in self.inputs if item.id not in [x["id"] for x in inputs]]
            print("****All the not needed inputs****")
            for input in oldInputs :
                print(input)

            updatedInputs = [updatedInput for updatedInput in inputs if updatedInput["id"] in [x.id for x in self.inputs]]
            print("****All the updated inputs****")
            for input in updatedInputs :
                print(input)
            
            newInputs = list(filter(lambda x: x['id'] is  None, inputs))
            print("****New inputs****")
            for input in newInputs :
                print(input)
            
            for input in oldInputs :
                input.delete(force=True)
            for input in newInputs: 
                newOne = Inputs().create(label=input["label"],type=input["type"],scriptID=self.id,incidentID=None,addedBy=addedBy)
                db.session.commit()
                steps = Steps().query.filter_by(scriptID=self.id).all()
                for step in steps :
                    inputInStep = InputsInStep().create(step=step.id,parentInput=newOne.id,order=len(self.inputs))
                    db.session.add(inputInStep)
                    step.inputs.append(inputInStep)
                # ----------------------------- adding new inputs ---------------------------- #
            for input in updatedInputs:
                Inputs().getInputByID(input["id"]).update(label=input["label"],type=input["type"],script=self)
    def getInputWithLabel(self,label):
        return next((input for input in self.inputs if input.label == label), None)

class Commands(db.Model):
    # ---------------------------- table configuration --------------------------- #
    __tablename__ = "commands"
    # -------------------------------- primary key ------------------------------- #
    id = db.Column(db.Integer,primary_key = True)
    # -------------------------------- Attributes -------------------------------- #
    keyWord = db.Column(db.String(15),nullable=False)
    paramsKeyWord = db.Column(db.String(15),nullable=False)
    #add need attribute params included by default to make it work with paramsKeyWord included by default
    #because for exemple execution on bash container needs -c attribute with or without inputs
    forContainers = db.Column(db.Boolean,default=False)
    forServers = db.Column(db.Boolean,default=False)
    # ------------------------------- Enum classes ------------------------------- #
    language = db.Column(db.Enum(languages),nullable = False)
    # ------------------------------- Foreing keys ------------------------------- #
    addedBy = db.Column(db.Integer,db.ForeignKey('users.id'))
    # ---------------------------- Giving foreing keys --------------------------- #
    steps = db.relationship("Steps",backref="command_relation")
    # ------------------------------ Static methods ------------------------------ #
    @staticmethod
    def getCommandByID(id):
        return Commands().query.filter_by(id=id).first()
    @staticmethod
    def listAll(keyWord=True,paramsKeyWord=True,FOR=True,language=True,addedBy=True):
        return [command.toDictionary(keyWord=keyWord,paramsKeyWord=paramsKeyWord,FOR=FOR,language=language,addedBy=addedBy) for command in Commands().query.all()]
    @staticmethod
    def checkIfKeyWordCombinationExists(keyWord,paramsKeyWord):
        return Commands().query.filter_by(keyWord=keyWord,paramsKeyWord=paramsKeyWord).first()
    @staticmethod
    def create(keyWord,paramsKeyWord,forContainers,forServers,language,addedBy):
        if Commands().checkIfKeyWordCombinationExists(keyWord,paramsKeyWord):
            raise ValueError("This command already exists.")
        command = Commands(keyWord=keyWord,paramsKeyWord=paramsKeyWord,forContainers=forContainers,forServers=forServers)
        # ------------------------------ handeling user ------------------------------ #
        if isinstance(addedBy,Users) :
            command.addedBy = addedBy.id
        elif Users().getUserByID(addedBy):
            command.addedBy = addedBy
        else:
            raise ValueError("User does not exist.")
        # ---------------------------- handeling language ---------------------------- #
        if attributeInEnum(language,languages):
            command.language = language
        else:
            raise ValueError(f'Language {language} is not supported please contact your support.')
        db.session.add(command)
    @staticmethod
    def selectCommand(onServer,language):
        if onServer:
            return Commands().query.filter_by(language=language,forServers= True ).first()
        else :
            return Commands().query.filter_by(language=language,forServers= False ).first()

    # ---------------------------------- methods --------------------------------- #
    def toDictionary(self,keyWord=True,paramsKeyWord=True,FOR=True,language=True,addedBy=True):
        return {
            "id" : self.id,
            "keyWord" : self.keyWord if keyWord else None,
            "paramsKeyWord" : self.paramsKeyWord if paramsKeyWord else None,
            "forContainers" : self.forContainers if FOR else None,
            "forServers" : self.forServers if FOR else None,
            "language" : self.language.value if language else None,
            "addedBy" : Users().getUserByID(self.addedBy).user if addedBy else None
        }
    def delete(self):
        if self.steps:
            raise ValueError("You cannot delete this command, it is still used in steps.")
        db.session.delete(self)
    def update(self,keyword,paramsKeyWord,forContainers,forServers,language):
        if keyword :
            if Commands().checkIfKeyWordCombinationExists(keyword,self.paramsKeyWord):
                raise ValueError("Command with this configuration already exists.")
            self.keyWord = keyword
        if paramsKeyWord :
            if Commands().checkIfKeyWordCombinationExists(self.keyWord,paramsKeyWord):
                raise ValueError("Command with this configuration already exists.")
            self.paramsKeyWord = paramsKeyWord
        if forContainers is not None :
            self.forContainers = forContainers
        if forServers is not None :
            self.forServers = forServers
        if language : 
            if attributeInEnum(language,languages):
                self.language = language
            else:
                raise ValueError(f'Language {language} is not supported please contact your support.')

class Inputs(db.Model):
    # -------------------------------- Primary key ------------------------------- #
    id = db.Column(db.Integer,primary_key = True)
    # -------------------------------- Attributes -------------------------------- #
    label = db.Column(db.String(256),nullable=False)
    type = db.Column(db.Enum(InputType),nullable = False)
    # ------------------------------- Foreing keys ------------------------------- #
    scriptID = db.Column(db.Integer,db.ForeignKey("scripts.id"))
    incidentID = db.Column(db.Integer,db.ForeignKey("incidents.id"))
    addedBy = db.Column(db.Integer,db.ForeignKey("users.id"))
    # ---------------------------- Foreing keys giver ---------------------------- #
    inputsInStep = db.relationship("InputsInStep",backref="inputs_relation",cascade="all,delete",lazy=True)
    # ------------------------------ Static methods ------------------------------ #
    @staticmethod
    def checkInputLabelScriptExist(script,label):
        return Inputs().query.filter_by(scriptID=script,label=label).first()
    @staticmethod
    def checkInputLabelIncidentExist(incident,label):
        return Inputs().query.filter_by(incidentID=incident,label=label).first()
    @staticmethod
    def getInputByID(id):
        return Inputs().query.filter_by(id=id).first()
    @staticmethod
    def create(label,type,scriptID,incidentID,addedBy):
        input = Inputs(label=label)
        # ------------------------------ handeling user ------------------------------ #
        if isinstance(addedBy,Users) :
            input.addedBy = addedBy.id
        elif Users().getUserByID(addedBy):
            input.addedBy = addedBy
        else:
            raise ValueError("User does not exist.")
        # ----------------------------- handeling script ----------------------------- #
        if scriptID is not None :
            if isinstance(scriptID,Scripts):
                input.scriptID = scriptID.id
            elif Scripts().getScriptByID(scriptID):
                    input.scriptID = scriptID
            else:
                raise ValueError("Script does not exist.")
        # ---------------------------- handeling incidents --------------------------- #
        elif incidentID is not None:
            if isinstance(incidentID,Incidents):
                input.incidentID = incidentID.id
            elif Incidents().getIncidentByID(incidentID):
                input.incidentID = incidentID
            else:
                raise ValueError("Incident does not exist.")
        else:
            raise ValueError("An input belongs to a script or an incident.")
        # ------------------------------ handeling type ------------------------------ #
        if attributeInEnum(type,InputType):
            input.type = type
        else:
            raise ValueError(f'Type {type} is not supported please contact your support.')
        db.session.add(input)
        return input
    @staticmethod
    def listAll():
        inputs = Inputs().query.all()
        return [input.toDictionary() for input in inputs]
    @staticmethod
    def getParallelInputForScript(label,script):
        script = Scripts().getScriptByID(script)
        if not script:
            raise ValueError("Script does not exist.")
        inputs = script.inputs
        for input in inputs:
            if input.label.lower() == label.lower():
                return input 
        return None
    @staticmethod
    def getParallelInputForIncident(label,incident):
        incident = Incidents().getIncidentByID(incident)
        if not incident:
            raise ValueError("Incident does not exist.")
        inputs = incident.inputs
        for input in inputs:
            if input.label.lower() == label.lower():
                return input 
        return None
    # ---------------------------------- Methods --------------------------------- #
    def delete(self,force=False):
        print(self.inputsInStep)
        if force is False and self.inputsInStep :
            raise ValueError("You cannot delete this input since it's already used in a step.")
        db.session.delete(self)
    def toDictionary(self):
        return {
            "id" : self.id,
            "label" : self.label,
            "type" : self.type.value,
            "scriptID" : self.scriptID,
            "incidentID" : self.incidentID,
            "addedBy" : Users().getUserByID(self.addedBy).user,
        }
    def update(self,label,type,script=None,incident=None):
        if script is not None:
            steps = script.steps
            for step in steps :
                inputsInStep = InputsInStep().listAllForStep(step.id)
                for inputInStep in inputsInStep:
                    if inputInStep['fromIncident'] is True :
                        for input in script.inputs :
                            if input.label == inputInStep["label"] and label != inputInStep["label"] :
                                print("here 2")
                                print(inputInStep)
                                print(input.toDictionary())
                                input.label = label 

                                print(input.toDictionary())

                                inputInStepToUpdateParent = InputsInStep().query.filter_by(id=inputInStep["id"]).first()
                                inputInStepToUpdateParent.parentInput = script.id

                                print(inputInStepToUpdateParent.toDictionary())
                                return

                                # raise ValueError(f'You cannot update the {input.label} input since is used as global in an incident.') 
        
        if incident is not None:
            steps = incident.steps
            for step in steps :
                inputsInStep = InputsInStep().listAllForStep(step.id)
                for inputInStep in inputsInStep:
                    if inputInStep['fromIncident'] is True :
                        for input in incident.inputs :
                            if input.label == inputInStep["label"] and label != inputInStep["label"] :
                                print("here")
                                print(inputInStep)
                                print(input.toDictionary())
                                input.label = label 

                                print(input.toDictionary())

                                inputInStepToUpdateParent = InputsInStep().query.filter_by(id=inputInStep["id"]).first()
                                inputInStepToUpdateParent.parentInput = step.scriptID

                                print(inputInStepToUpdateParent.toDictionary())

                                return
                                # raise ValueError(f'You cannot update the {input.label} input since is used as global in an incident.') 
        
        if self.scriptID is not None and self.incidentID is None :
            if self.label != label and Inputs().checkInputLabelScriptExist(self.scriptID,label):
                raise ValueError(f'Input with the label {label} already exists.')
            self.label = label
        else :
            if self.label != label and Inputs().checkInputLabelIncidentExist(self.incidentID,label):
                raise ValueError(f'Input with the label {label} already exists.')
            # self.incidentID = None
            # self.scriptID = script.id
            self.label = label
        # ------------------------------ handeling type ------------------------------ #
        if attributeInEnum(type,InputType):
            self.type = InputType[type.upper()] 
        else:
            raise ValueError(f'Type {type} is not supported please contact your support.')

class InputsInStep(db.Model):
    # -------------------------------- Primary key ------------------------------- #
    id = db.Column(db.Integer,primary_key = True)
    # -------------------------------- Attributes -------------------------------- #
    required = db.Column(db.Boolean,nullable = False)
    order = db.Column(db.Integer,nullable = False) #This attribute need to be check if it's necessary
    # -------------------------------- Foreing key ------------------------------- #
    step = db.Column(db.Integer, db.ForeignKey('steps.id', ondelete='RESTRICT'))
    parentInput = db.Column(db.Integer, db.ForeignKey('inputs.id', ondelete='RESTRICT'))
    # ------------------------------- Static method ------------------------------ #
    @staticmethod
    def listAllForStep(step):
        inputs = InputsInStep().query.filter_by(step=step)
        return [input.toDictionary() for input in inputs]
    @staticmethod
    def create(step,parentInput,order):
        inputStep = InputsInStep(required=True)
        # ------------------------------ handeling step ------------------------------ #
        if step is not None:
            if not Steps().getStepByID(step):
                raise ValueError('Step does not exist.')
            inputStep.step = step
        # -------------------------- handeling parent input -------------------------- #
        print("looking for parent input",parentInput)
        if not Inputs().getInputByID(parentInput):
            print("inputs parent id not found",parentInput)
            raise ValueError("Input does not exist.")
        inputStep.parentInput = parentInput
        # ------------------------------ handeling order ----------------------------- #
        if order < 0 :
            raise ValueError("Step input order must be positif.")
        inputStep.order = order
        db.session.add(inputStep)
        return inputStep
    @staticmethod
    def getInputByID(id):
        return InputsInStep().query.filter_by(id=id).first()
    @staticmethod
    def getInputsByIncidentID(incident):
        return InputsInStep().query.filter_by(parentInput=incident).all()
    # ---------------------------------- Methods --------------------------------- #
    def delete(self):
        db.session.delete(self)
    def toDictionary(self):
        Pinput = Inputs().getInputByID(self.parentInput)
        return {
            "id" : self.id,
            "required" : self.required,
            "order" : self.order,
            "step" : self.step,
            "parentInput" : self.parentInput,
            "label" : Pinput.label,
            "fromIncident" : True if Pinput.incidentID is not None else False,
            "type" : Pinput.type.value,
        }
    def update(self,incident=None,script=None):
        if incident is None and script is None:
            raise ValueError("Cannot update input in step, please select where it should come from.")
        elif incident is not None and script is not None:
            raise ValueError("Cannot update input in step, please select one source where it should come from.")
        elif incident is not None :
            self.parentInput = incident
        elif script is not None :
            self.parentInput = script

class Incidents(db.Model):
    # ------------------------------- Primary keys ------------------------------- #
    id = db.Column(db.Integer,primary_key = True)
    # -------------------------------- Attributes -------------------------------- #
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text , nullable = False)
    # ------------------------------- Foreing keys ------------------------------- #
    addedBy = db.Column(db.Integer,db.ForeignKey("users.id"))
    # ---------------------------- Foreing keys giver ---------------------------- #
    steps = db.relationship("Steps", backref="incident_relation",order_by='Steps.order',cascade="all,delete",lazy=True)
    inputs = db.relationship("Inputs",backref="incident_relation",cascade="all,delete",lazy=True)
    # ------------------------------ Static methods ------------------------------ #
    @staticmethod
    def getIncidentByID(id):
        return Incidents().query.filter_by(id=id).first()
    @staticmethod
    def listAll(steps,inputs,query_name=None):
        incidents = Incidents().query
        if query_name is None :
            incidents = incidents.all()
        else :
            incidents = incidents.filter(Incidents.name.ilike(f'%{query_name}%'))
        return [incident.toDictionary(steps,inputs) for incident in incidents]
    @staticmethod
    def create(name,description,inputs,addedBy):
        if Incidents().checkIfIncidentNameExist(name):
            raise ValueError(f'Incident {name} already exist.')
        if len(name) < 3 :
            raise ValueError(f'Incident name {name} too short.')

        incident = Incidents(name=name)
        # --------------------------- handeling description -------------------------- #
        if len(description) == 0 :
            raise ValueError("Description cannot be empty.")
        incident.description = description
        # ------------------------------ handeling user ------------------------------ #
        if isinstance(addedBy,Users) :
            incident.addedBy = addedBy.id
        elif Users().getUserByID(addedBy):
            incident.addedBy = addedBy
        else:
            raise ValueError("User does not exist.")
        # -------------------------- handeling global inputs ------------------------- #
        db.session.add(incident)
        db.session.commit()
        for input in inputs :
            db.session.add(Inputs().create(label=input['label'],type=input['type'],scriptID=None,incidentID=incident.id,addedBy=addedBy)) 
        return incident
    @staticmethod
    def checkIfIncidentNameExist(name):
        return Incidents().query.filter_by(name=name).first()
    # ---------------------------------- Methods --------------------------------- #
    def delete(self):
        db.session.delete(self)
    def toDictionary(self,steps=False,inputs=False,description=True,name=True,addedBy=True):
        return{ 
            "id" : self.id ,
            "name" : self.name if name else None,
            "description" : self.description if description else None,
            "addedBy" : Users().getUserByID(self.addedBy).user if addedBy else None,
            "steps" : [step.toDictionary(server=True,script=True) for step in self.steps] if steps else None,
            "inputs" : [input.toDictionary() for input in self.inputs] if inputs else None,
        }
    def update(self,name,description,steps,inputs,addedBy):
        if name is not None :
            if Incidents().checkIfIncidentNameExist(name):
                raise ValueError(f'Incident {name} already exist.')
            self.name= name 
        if description is not None :
            if len(description) == 0 :
                raise ValueError("Description cannot be empty.")
            self.description = description
        if inputs is not None : 
            oldInputs = [item for item in self.inputs if item.id not in [x["id"] for x in inputs]]
            updatedInputs = [updatedInput for updatedInput in inputs if updatedInput["id"] in [x.id for x in self.inputs]]
            newInputs = list(filter(lambda x: x['id'] is  None, inputs))
            
            for input in oldInputs :
                input.delete(force=False)
            
            for input in newInputs: 
                db.session.add(Inputs().create(label=input["label"],type=input["type"],scriptID=None,incidentID=self.id,addedBy=addedBy))
            
            for input in updatedInputs:

                Inputs().getInputByID(input["id"]).update(label=input["label"],type=input["type"],incident=self)
        if steps is not None:
            oldSteps = [item for item in self.steps if item.id not in [x["id"] for x in steps]]
            updatedSteps = [updatedStep for updatedStep in steps if updatedStep["id"] in [x.id for x in self.steps]]
            
            for step in oldSteps :
                step.delete()
            for step in updatedSteps:
                Steps().getStepByID(step["id"]).update(order=step['order'])
    def getInputWithLabel(self,label):
        return next((input for input in self.inputs if input.label == label), None)

class Users(db.Model):
    # ------------------------------- Primary keys ------------------------------- #
    id = db.Column(db.Integer,primary_key = True)
    # -------------------------------- Attributes -------------------------------- #
    user = db.Column(db.String(50),nullable=False,unique=True)
    account_active = db.Column(db.Boolean,default=True)
    can_execute = db.Column(db.Boolean,default=False)
    is_admin = db.Column(db.Boolean,default=False)
    # ---------------------------- Foreing keys giver ---------------------------- #
    servers = db.relationship('Servers',backref="addedBy_relation",lazy=True) 
    containers = db.relationship("Containers",backref="addedBy_relation",lazy=True)
    scripts = db.relationship("Scripts",backref="addedBy_relation",lazy=True)
    inputs = db.relationship("Inputs",backref="addedBy_relation",lazy=True)
    incidents = db.relationship("Incidents",backref="addedBy_relation",lazy=True)
    steps= db.relationship("Steps",backref="addedBy_relation",lazy=True)
    commands= db.relationship("Commands",backref="addedBy_relation",lazy=True)
    # ------------------------------ Static methods ------------------------------ #
    @staticmethod
    def getUserByID(id):
        return Users().query.filter_by(id=id).first()
    @staticmethod
    def create(username,admin=False,execute=False):
        if Users().checkIfUserNameExist(username.lower()) :
            raise ValueError(f'Username: {username} already used')
        user = Users(user=username)
        if admin is True :
            user.can_execute = True
            user.is_admin = True
        if execute is True :
            user.can_execute = True
        db.session.add(user)
        return user
    @staticmethod
    def checkIfUserNameExist(username):
        return Users().query.filter_by(user=username).first()
    @staticmethod
    def ToStringUsers(users):
        res = []
        for user in users :
            res.append(user.toString())
        return res 
    @staticmethod
    def listAll(query_name=None):
        users = Users().query
        if query_name is not None :
            users = users.filter(Users.user.ilike(f'%{query_name}%'))
        else :
            users = users.all()
        return [user.toDictionary() for user in users]
    # ---------------------------------- Methods --------------------------------- #
    def disableUser(self):
        print("actual users num",len(Users().query.filter().all()))
        if len(Users().query.filter_by(account_active=True).all()) <= 1 :
            raise ValueError("At least one user must stay active!")
        self.DisableAdminPrivlege()
        self.disableUserExecute()
        self.account_active = False
    def activeUser(self):
        self.account_active = True
    def enableUserExecute(self) :
        self.can_execute = True
    def disableUserExecute(self) :
        self.can_execute = False
    def delete(self):
        if self.AddedByServers or self.AddedByContainers or self.AddedByScripts or self.AddedByInputs or  self.AddedByIncidents or   self.AddedBySteps :
            self.disableUser()
        else:
            db.session.delete(self)
    def toDictionary(self):
        return {
            'id' : self.id,
            'username' : self.user,
            'active' : self.account_active,
            'execute' : self.can_execute,
            "admin" : self.is_admin
        }
    def setEnableAdminPrivlege(self):
        self.is_admin = True
    def DisableAdminPrivlege(self):
        self.is_admin = False
    def update(self,username=None,admin=None,execute=None,active=None):
        if username is not None :
            user = Users().checkIfUserNameExist(username)
            if user and user.id != self.id :
                raise ValueError(f'User with the username {username} already exists.')
            self.user = username
        if admin is not None :
            self.is_admin =admin
        if execute is not None :
            self.can_execute =execute 
