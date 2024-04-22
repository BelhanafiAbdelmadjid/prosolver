from flask import session , request ,jsonify
from main import  app , ExpectedServersUAT , ExpectedServersPROD 
from main.Command import *
from main.Models import Users, Servers, Containers, Scripts, Inputs, Incidents, Steps ,InputType , InputsInStep
from main import db , ldap
from functools import wraps
import re
import datetime
from main.SSH import SSH 

# ---------------------------------------------------------------------------- #
#                             Routes configuration                             #
# ---------------------------------------------------------------------------- #
@app.before_request
def makeSessionTemp():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=60)

@app.after_request
def after_request(response):
    return response

@app.route('/')
def index():
    return 'Hello, World!'

@app.errorhandler(500)
def server_error(error):
    app.logger.exception('An exception occurred during a request.'+str(error))
    return 'Internal Server Error', 500



# ---------------------------------------------------------------------------- #
#                               Wrapper functions                              #
# ---------------------------------------------------------------------------- #
def check_login(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        # Perform pre-route logic or checks here
        # ...
        # If the condition is not met, return a specific response
        for s in session :
            print(s)
        if(len(session) <= 1):
            return jsonify({'error': 'not authentificated'}) , 401
        # Otherwise, continue with the route handler function
        return func(*args, **kwargs)
    return wrapped_func

def check_execution_habilitation(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        userID = loadUser()
        user = Users().getUserByID(userID)
        if not user.can_execute :
            return jsonify({"msg" : f'User {user.user} is not authorized to execute, please reach to an admin.'}) , 403
        return func(*args, **kwargs)
    return wrapped_func

def check_if_execution_in_process(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        if 'executing' in session :
            return jsonify({"msg" : f'You can execute one step at a time, please wait for the {session["executing"]["step"]} to finish.'}),400
        return func(*args, **kwargs)
    return wrapped_func

def check_admin_privilege(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        userID = loadUser()
        user = Users().getUserByID(userID)
        if not user.is_admin :
            return jsonify({"msg" : f'User {user.user} is not authorized to do this action, please reach to an admin.'}) , 403
        return func(*args, **kwargs)
    return wrapped_func

def check_login_UAT(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        # Perform pre-route logic or checks here
        # ...
        # If the condition is not met, return a specific response
        if(len(session) <= 1 or not "AUTH_UAT" in session):
            return jsonify({'error': 'not authentificated'}) , 401
        # Otherwise, continue with the route handler function
        return func(*args, **kwargs)
    return wrapped_func

def check_login_PROD(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        # Perform pre-route logic or checks here
        # ...
        # If the condition is not met, return a specific response
        if(len(session) <= 1 or not "AUTH_PROD" in session ):
            return jsonify({'error': 'not authentificated'}) , 401
        # Otherwise, continue with the route handler function
        return func(*args, **kwargs)
    return wrapped_func

def checkIfAdmin(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        if "AUTH_PROD" in session :
            username = session["AUTH_PROD"]["username"]
        if "AUTH_UAT" in session :
            username = session["AUTH_UAT"]["username"]
        if not Users.query.filter_by(user=username).first() :
            return jsonify({"msg" : "Action not allowed please reach to an admin"}),  403
        return func(*args, **kwargs)
    return wrapped_func
   


# ---------------------------------------------------------------------------- #
#                            Authentification routes                           #
# ---------------------------------------------------------------------------- #
@app.get("/api/UAT/logedin")
@check_login_UAT
def logedinUAT():
    return jsonify({
        "username" : session["AUTH_UAT"]["username"]
    }),200

@app.get("/api/login/informations")
@check_login_UAT
def getLoginInformation():
    user = loadUser()
    user = Users().query.filter_by(id=user).first()
    return jsonify({
        "username" : user.user,
        "userType" : "Admin" if user.is_admin else ("Worker" if user.can_execute else "Viewer" ),
        "connexionType" : {
            "UAT" : True if 'AUTH_UAT' in session else False,
            "PROD" : True if 'AUTH_PROD' in session else False,
        }
    }),200

@app.post("/api/UAT/disconnect")
@check_login_UAT
def defaultRouteUAT():
    del session["AUTH_UAT"]
    return jsonify({'msg' : 'Disconnected for UAT view.'}) ,200

@app.post("/api/disconnect")
def disconnect():
    session.clear()
    return jsonify({'msg' : 'Disconnected.'}) ,200

@app.post("/api/UAT/login")
def LoginUAT():
    data = request.get_json()
    username = data["username"]
    user = Users().checkIfUserNameExist(username)
    if not user :
        return jsonify({'msg' : 'Acces not allowed please contact support.'}) , 403
    if not user.account_active :
        return jsonify({'msg' : 'User disabled please contact support.'}) , 403

    password = data["password"]
    try:
        # initialisationConnexionRandom(username,password,ExpectedServersUAT)
        print(username,password)
        if ldap.authentificate(username,password) is False :
            return jsonify({'msg' : "Please check your credentials or contact your support."}) , 400
        userInfo = {
                "username" : username,
                "password" : password,
            }
        session["AUTH_UAT"] = userInfo
        user = Users().query.filter_by(user=username).first()
        response = {"msg" : "logged in"
                    ,"admin" : True if user else False
                    }
        return jsonify(response) ,200
    except Exception as e :
        print(e)
        return jsonify({'msg' : "an error has occured"}) , 400

@app.get("/api/Prod/logedin")
@check_login_PROD
def logedin():
    if session["AUTH_PROD"] :
        return  {"LoggedIn" : True ,
                "username" : session["AUTH_PROD"]["username"]
                } , 200

@app.get("/api/Prod/disconnect")
@check_login_PROD
def defaultRoute():
    del session["AUTH_PROD"]
    return jsonify({'msg' : 'session cleared'}) ,200

@app.post("/api/Prod/login")
def Login():
    data = request.get_json()
    username = data["username"] 
    user = Users().checkIfUserNameExist(username)
    if not user :
        return jsonify({'msg' : 'Acces not allowed please contact support.'}) , 403
    if not user.account_active :
        return jsonify({'msg' : 'User disabled please contact support.'}) , 403
    password = data["password"]
    try:
        initialisationConnexionRandom(username,password,ExpectedServersPROD)
        userInfo = {
                "username" : username,
                "password" : password,
            }
        session["AUTH_PROD"] = userInfo
        response = {"msg" : "logged in"}
        return jsonify(response) ,200
    except Exception as e :
        return jsonify({'msg' : "an error has occured"}) , 400



# ---------------------------------------------------------------------------- #
#                                  //Functions                                 #
# ---------------------------------------------------------------------------- #
def loadUser():
    if "AUTH_PROD" in session :
        username = session["AUTH_PROD"]["username"]
    if "AUTH_UAT" in session :
        username = session["AUTH_UAT"]["username"]
    user = Users().query.filter_by(user=username).first()
    if user :
        return user.id
    return None











# ---------------------------------------------------------------------------- #
#                              //Incidents routes                              #
# ---------------------------------------------------------------------------- #
# ------------------------------- admin routes ------------------------------- #
@app.post("/api/incident/create")
@check_login
@check_admin_privilege
def createIncident():
    data = request.get_json()

    name = str(data["name"])
    description = data["description"]
    globalInputs = data["inputs"]
    user = loadUser()

    try :
        incident=Incidents().create(name=name,description=description,inputs=globalInputs,addedBy=user)
        db.session.commit()
        return jsonify({'msg' : f'Incident {incident.name} created successfully.',
                        'id' : incident.id}) , 200
    except Exception as e:
        return jsonify({'msg' : str(e)}) , 400

@app.delete("/api/incident/delete")
@check_login
@check_admin_privilege
def IncidentDelete():
    data = request.get_json()
    id = data["id"]
    incident = Incidents().getIncidentByID(id)
    if not incident :
        return jsonify({"msg" : "Incident does not exist."}) , 400
    try : 
        incident.delete()
        db.session.commit()
        return jsonify({"msg" : "Incident deleted successfully"}) , 200
    except Exception as e :
        return jsonify({"msg" : str(e)}) , 400
    
@app.put("/api/incident/update")
@check_login
@check_admin_privilege
def incidentUpdate():
    data = request.get_json()
    incident = data["id"]
    incident = Incidents().getIncidentByID(incident)
    if not incident :
        return jsonify({'msg' : 'Incident does not exist.'}),400
    
    name = None
    description = None
    inputs = None
    steps = None

    if "name" in data:
        name = data["name"]
    if 'description' in data :
        description = data["description"]
    if 'inputs' in data:
        inputs = data["inputs"]
    if 'steps' in data:
        steps = data["steps"]
    user = loadUser()
    try :
        incident.update(name=name,description=description,addedBy=user,steps=steps,inputs=inputs)
        db.session.commit()
        return jsonify({'msg' : f'Incident {incident.name} updated successfully.'}) , 200
    except Exception as e :
        return jsonify({'msg':str(e)}) , 400



# ------------------------------- users routes ------------------------------- #
@app.get("/api/incidents")
@check_login
def getIncidents():
    # time.sleep(5)
    return jsonify(Incidents().listAll(steps=False,inputs=False,query_name=request.args.get("name"))) , 200

@app.get("/api/incident/<id>")
@check_login
def getIncident(id):
    incident = Incidents().getIncidentByID(id)
    if not incident :
        return jsonify({"msg" : "An error has occured."}) , 400
    return jsonify(incident.toDictionary(steps=True,inputs=True)),200

@app.get("/api/incident/<id>/step/create")
@check_login
@check_admin_privilege
def stepCreateVue(id):
    incident = Incidents().getIncidentByID(id)
    if not incident :
        return jsonify({'msg' : "Incident does not exist."}),400
    return jsonify(Steps().stepCreateVue(incident)) , 200
    


# ---------------------------------------------------------------------------- #
#                                //Steps routes                                #
# ---------------------------------------------------------------------------- #
# ------------------------------- admin routes ------------------------------- #
@app.post("/api/incident/step/create")
@check_login
@check_admin_privilege
def newStep():
    data = request.get_json()
    
    container = None
    inputs = None

    incident = data["incident"]
    server = data["server"]
    script = data["script"]
    name = data["name"]


    if 'container' in data :
        container = data["container"]
        onServer = False if container is not None else True
        print("SETING UP onServer with container ",container)
    if 'inputs' in data :    
        inputs = data["inputs"]
    user = loadUser()

    try :
        step = Steps().create(name=name,server=server,script=script,onServer=onServer,container=container,inputs=inputs,incident=incident,addedBy=user)
        db.session.commit()
        return jsonify({'msg' :f'Step {step.name} created successfully.'}) , 200
    except Exception as e :
        return jsonify({'msg' : str(e)}) , 400

@app.put("/api/incident/step/update")
@check_login
@check_admin_privilege
def updateStep():
    data = request.get_json()
    step = data["step"]
    print(data)
    server = None
    script = None
    container = None
    name = None
    inputInStep = None
    onServer = None
    user = loadUser()

    if 'server' in data :
        server = data["server"]
    if 'script' in data :
        script = data["script"]
    if 'container' in data :
        container = data["container"]
    if 'name' in data :
        name = data["name"]
    if 'onServer' in data :
        onServer = data["onServer"]
    if 'inputs' in data :
        inputInStep = data["inputs"]

    
    step = Steps().getStepByID(step)
    if not step :
        return jsonify({'msg' : 'Step does not exist.'}) , 400
    try :
        step.update(
        name=name,
        order=None,
        script=script,
        onServer=onServer,
        server=server,
        container=container,
        inputs = inputInStep,
        addedBy=user
        )
        db.session.commit()
        return jsonify({'msg' : 'Step updated successfuly.'}) , 200
    except Exception as e :
        return jsonify({'msg' : str(e)}) , 400

@app.delete("/api/incident/step/delete")
@check_login
@check_admin_privilege
def removeStep():
    data = request.get_json()
    incident = data["incident"]
    step = data["id"]
    if not Incidents().query.filter_by(id=incident):
        return jsonify({"msg" : "Incident does not exist"}) , 400
    try :
        step = Steps().getStepByID(step)
        if not step :
            raise ValueError("Step does not exist.")
        step.delete()
        db.session.commit()
        return jsonify({"msg" : "Step succesfully removed."}) , 200
    except Exception as e :
        return jsonify({'msg' : str(e)}) , 400

# ---------------------------- habilitation routes --------------------------- #
@app.post("/api/incident/step/execute")
@check_login
@check_execution_habilitation
@check_if_execution_in_process
def executeStepInServer():
    data = request.get_json()
    session["executing"] = {}
    step = data["id"]
    inputs = data["inputs"]
    
    step = Steps().getStepByID(step)
    if not step :
        del session["executing"]
        return jsonify({'msg' : 'Step does not exist.'}),400
    
    session["executing"] = {
            "step" : step.name,
        }

    try :
        result ,error = step.execute(userInputs=inputs,username=session["AUTH_UAT"]["username"],password=session["AUTH_UAT"]["password"])
        del session["executing"]
        user = loadUser()
        user = Users().query.filter_by(id=user).first()
        print("here",''.join([ f'{input["label"]} {input["value"]}' for input in inputs] ))
        # app.logger.info(f'INFO EXECUTION HEADER:  {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} user : {user.user} executed script ID: {step.scriptID} with inputs in order : {''.join([ f'[{input["label"]} : {input["value"]}] ' for input in inputs] )} ')
        app.logger.warning(f'WARNING EXECUTION {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : {user.user}/{user.id} got an ERROR when executing script {step.scriptID} with inputs in order {''.join([ f'[{input["label"]} : {input["value"]}] ' for input in inputs] )} : \n {error}')
        app.logger.info(f'INFO EXECUTION {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : {user.user}/{user.id} got the result when executing script {step.scriptID} with inputs in order {''.join([ f'[{input["label"]} : {input["value"]}] ' for input in inputs] )} : \n {result}')
        print(type(error))
        res = {"result" : result}
        if error and result :
            res["warning"] = error
        elif not result and error :
            res = {"error" : error}
        else :
            res["error"] = []
        print(res)
        return jsonify(res) , 200
    except Exception as e :
        print(e)
        if 'executing' in session:
            del session["executing"]
        return jsonify({"msg" : str(e)}) , 400

  
# ------------------------------- users routes ------------------------------- #
@app.get("/api/incident/<incident>/step/<step>")
@check_login
def getStep(incident,step):
    incident = Incidents().getIncidentByID(incident)
    if not incident :
        return jsonify({'msg' : 'Incident does not exist.'}) , 400
    step = Steps().getStepByID(step)
    if not step :
        return jsonify({'msg' : 'Step does not exist.'}) , 400
    return jsonify(step.toDictionary(server=True,script=True)),200

@app.get("/api/step/<step>")
@check_login
def getStepToEdit(step):
    step = Steps().getStepByID(step)
    if not step :
        return jsonify({'msg' : 'Step does not exist.'}) , 400
    return jsonify({
        "step" : step.toDictionary(server=True,script=True),
        "servers" : Servers().listAll(addedBy=False,containers=True),
        "scripts" : Scripts().listAll(content=False,name=True,inputs=True)
    }),200

@app.get("/api/incident/<incident>/steps")
@check_login
def getIncidentSteps(incident):
    incident = Incidents().getIncidentByID(incident)
    if not incident :
        return jsonify({'msg' : 'Incident does not exist.'}) , 400
    return jsonify([step.toDictionary(True) for step in incident.steps]),200

@app.get("/api/incident/<incident>/script/<script>/join")
@check_login
def getIncidentScriptInputsJoin(incident,script):
    incident = Incidents().getIncidentByID(incident)
    if not incident:
        return jsonify({'msg' : 'Incident does not exist.'}),400
    script = Scripts().getScriptByID(script)
    if not script:
        return jsonify({'msg' : 'Script does not exist.'}),400
    return jsonify(Steps().joinInputsIncidentStep(incident=incident,script=script)),200

@app.get("/api/incident/<incident>/script/<script>/join/<step>")
@check_login
def getInputsJoinOrOldOnes(incident,script,step):
    incident = Incidents().getIncidentByID(incident)
    if not incident:
        return jsonify({'msg' : 'Incident does not exist.'}),400
    script = Scripts().getScriptByID(script)
    if not script:
        return jsonify({'msg' : 'Script does not exist.'}),400
    step = Steps().getStepByID(step)
    if not step:
        return jsonify({'msg' : 'Step does not exist.'}),400
    
    return jsonify(step.joinInputsOrGetOldOnes(incident=incident,script=script)),200





# ---------------------------------------------------------------------------- #
#                               //Servers routes                               #
# ---------------------------------------------------------------------------- #

# ------------------------------- admin routes ------------------------------- #
@app.post("/api/server/create")
@check_login
@check_admin_privilege
def addServer():
    data = request.get_json()
    ip = data["ip"]
    name = data["name"]
    type = data["type"]
    addedBy= loadUser()
    containers = data["containers"]
    try :
        server = Servers().create(name,type,ip,addedBy,containers)
        db.session.commit()
        return jsonify({
            'msg':"Server created successfully",
            "id" : server.id
            }) , 200
    except Exception as e :
        print(e)
        return jsonify({'msg':str(e)}) , 400

@app.delete("/api/server/delete")
@check_login
@check_admin_privilege
def deleteServer():
    data = request.get_json()
    id = data["id"]
    server = Servers().getServerByID(id)
    if not server:
        return jsonify({"msg" : "Server does not exist"}) , 400
    try :
        server.delete()
        db.session.commit()
        return jsonify({"msg" : "Server Deleted successfully"}) , 200
    except Exception as e :
        print(e)
        return jsonify({"msg" : str(e)}) , 400

@app.put("/api/server/edit")
@check_login
@check_admin_privilege
def serverEdit():
    data = request.get_json()

    server  = data["id"]

    server = Servers().getServerByID(server)
    if not server :
        return jsonify({"msg" : "Server does not exist."}) , 400
    
    user = loadUser()

    name = None
    ip = None 
    type= None 
    containers = None

    if "name" in data :
        name = data["name"] 
    if "ip" in data:
        ip = data["ip"] 
    if 'type' in data:
        type = data["type"]
    if "containers" in data :
        containers = data["containers"]
        print("receiving containers",containers)
    
    try:
        server.update(name,ip,type,containers,user)
        db.session.commit()
        return jsonify({"msg" : f'Server {server.name} updated succsessfully.'}),200
    except Exception as e:
        print(e)
        return jsonify({"msg" : str(e)}) , 400        

# ------------------------------ all users route ----------------------------- #
@app.get("/api/servers")
@check_login
def getServers():
    return jsonify(Servers().listAll(containers=True,ping=False,query_name=request.args.get("name"))) , 200

@app.get("/api/server/<id>")
@check_login
def getServer(id):
    return jsonify(Servers().getServerByID(id).toDictionary(containers=True,ping=False)) , 200


@app.get("/api/UAT/servers")
@check_login
def serversUATReachableStatus():
    print(request.args.get("name"))
    return jsonify(Servers().listUATServersSupervision(query_name=request.args.get("name"))) , 200

@app.get("/api/Prod/servers")
@check_login
def serversPRODReachableStatus():
    return jsonify(Servers().listProdServersSupervision(query_name=request.args.get("name"))) , 200



# ---------------------------------------------------------------------------- #
#                              //Containers routes                             #
# ---------------------------------------------------------------------------- #

# -------------------------------- admin route ------------------------------- #
@app.post("/api/server/container/create")
@check_login
@check_admin_privilege
def containerCreate():
    data = request.get_json()
    server = data["server"]
    name = data["name"]
    user = loadUser()
    try:
        Containers().create(name=name,server=server,addedBy=user)
        db.session.commit()
        return jsonify({"msg" : f'Container {name} created successfully.'}) , 200
    except Exception as e:
        return jsonify({"msg" : str(e)}) , 400

@app.delete("/api/server/container/delete")
@check_login
@check_admin_privilege
def deleteServersContainer():
    data = request.get_json()
    container = data["container"]
    server = data["server"]
    try :
        if not Servers().getServerByID(server):
            raise ValueError("Server does not exist") 
        Containers().deleteWithID(container)
        db.session.commit()
        return jsonify({"msg" : "Container delete successfully"}) , 200
    except Exception as e :
        print(e)
        return jsonify({"msg" : str(e)}) , 400

# -------------------------------- users route ------------------------------- #
@app.get("/api/server/<int:server>/containers")
@check_login
def getContainers(server):
    if not Servers().query.filter_by(id=server).first():
        return jsonify({"msg" : "Server does not exist."}) , 400
    return jsonify([container.toDictionary() for container in Containers().getContainersOfServer(server)]),200
# ------------------------------- SSH Commands ------------------------------- #()
@app.get("/api/server/<srv>/containers/status")
@check_login_UAT
def serverContainersStatus(srv):
    server = Servers().query.filter_by(id=srv).first()
    if server is not None:
        try :
            cmd = " docker ps --format 'table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}' "
            result = executeCommande(server.ip ,app.config.get("USER_APP") ,app.config.get("USER_APP_PASSWORD"),cmd)
            if len(result) == 0:
                return jsonify([]) , 200
            i = 0 
            dicT = []
            if result[-1] == "0":
                result.pop(-1)
            while i < len(result) :
                result[i] = re.split(r'\s{2,}',(result[i]))
                i = i + 1
            head = result[0]
            result.pop(0)
            
            for x in result :
                dict = {
                    head[0] : x[0],
                    head[1] : x[1],
                    head[2] : x[2],
                    head[3] : x[3],
                }
                dicT.append(dict)
            data = dicT
            
            return jsonify(data) , 200
        except Exception as e:
            return jsonify({"error" : str(e)}) , 404
        
    else :
        return jsonify({"error" : "Server does not exist found"}) , 404



# ---------------------------------------------------------------------------- #
#                               //Commands routes                              #
# ---------------------------------------------------------------------------- #
# ------------------------------- admin routes ------------------------------- #
@app.post("/api/command/create")
@check_login
@check_admin_privilege
def createCommand():
    data = request.get_json()

    keyword = data["keyword"]
    language = data["language"]
    paramsKeyWord = data["paramsKeyWord"]
    forContainers = data["forContainers"]
    forServers = data["forServers"]
    user= loadUser()

    try :
        Commands().create(keyword,paramsKeyWord,forContainers,forServers,language,addedBy=user)
        db.session.commit()
        return jsonify({"msg" : "Command created succsessfully."}) ,200
    except Exception as e :
        return jsonify({'msg' : str(e)}) , 400

@app.delete("/api/command/delete")
@check_login
@check_admin_privilege
def deleteCommand():
    data = request.get_json()
    command = data["command"]
    command = Commands().getCommandByID(command)
    if not command:
        return jsonify({'msg' : 'Command does not exist.'}) , 400
    try :
        command.delete()
        db.session.commit()
        return jsonify({'msg' : 'Command deleted succsesfully.'}) , 200
    except Exception as e :
        return jsonify({"msg" : str(e)}) , 400
    
@app.put("/api/command/edit")
@check_login
@check_admin_privilege
def updateCommand():
    data = request.get_json()

    command = data["id"]
    command = Commands().getCommandByID(command)
    if not command :
        return jsonify({"msg" : "Command does not exist."}),400

    keyword = None
    language = None
    paramsKeyWord = None
    forContainers = None
    forServers = None

    if 'keyword' in data:
        keyword = data["keyword"]
    if 'language' in data:    
        language = data["language"]
    if 'paramsKeyWord' in data:
        paramsKeyWord = data["paramsKeyWord"]
    if 'forContainers' in data:
        forContainers = data["forContainers"]
    if 'forServers' in data:
        forServers = data["forServers"]
    try : 
        command.update(keyword,paramsKeyWord,forContainers,forServers,language)
        db.session.commit()
        return jsonify({'msg' : 'Command successfully updated.'}) , 200
    except Exception as e :
        return jsonify({'msg' : str(e)}) , 200

# ------------------------------- users routes ------------------------------- #
@app.get("/api/commands")
@check_login
def getCommands():
    return jsonify(Commands().listAll()) , 200    

@app.get("/api/command/<int:id>")
@check_login
def getCommand(id):
    command = Commands().getCommandByID(id)
    if not command:
        return jsonify({"msg" : "Command does not exist."}),400
    return jsonify(command.toDictionary()),200



# ---------------------------------------------------------------------------- #
#                               //Scripts routes                               #
# ---------------------------------------------------------------------------- #
# ------------------------------- admin routes ------------------------------- #
@app.post("/api/script/create")
@check_login
@check_admin_privilege
def scriptCreate():
    data = request.get_json()
    
    name = data["name"]
    content = data["content"]
    description = data["description"]
    outPutLinesNumber = 999
    params = True if len(data["inputs"] )> 0 else False
    language = data["language"]
    inputs = data["inputs"]
    user = loadUser()

    if Scripts().getScriptByName(name):
        return jsonify({"msg" : f'Script {name} already exists.'}) , 400
    try :
        script = Scripts().create(name,outPutLinesNumber,description,content,params,language,inputs,addedBy=user)
        db.session.commit()
        return jsonify({
            'msg' : f'Scripts {name} successfully created.',
            'id' : script.id
            }) , 200
    except Exception as e :
        return jsonify({'msg' : str(e)}) , 400

@app.delete("/api/script/delete")
@check_login
# @check_admin_privilege
@check_admin_privilege
def removeScript():
    data = request.get_json()
    script = data["id"]
    try :
        script = Scripts().getScriptByID(script)
        if not script:
            raise ValueError("Script does not exist.")
        script.delete()
        db.session.commit()
        return jsonify({"msg" : "Script deleted successffuly"})
    except Exception as e :
        print(e)
        return jsonify({"msg" : str(e)}) , 400

@app.put("/api/script/edit")
@check_login
@check_admin_privilege
def editScript():
    data = request.get_json()
    script = data["id"]
    
    script = Scripts().getScriptByID(script)
    if not script :
        return jsonify({"msg" : "Script does not exist."}) , 400
    
    content = None
    name = None
    language = None
    outPutLinesNumber = None
    inputs = None
    description = None
    params = None
    user = loadUser()

    if "content" in data :
        content = data["content"]
    if 'name' in data :
        name = data["name"]
    if 'outPutLinesNumber' in data :
        outPutLinesNumber = data["outPutLinesNumber"]
    if 'inputs' in data :
        inputs = data["inputs"]
    if 'description' in data :
        description = data["description"]
    if 'params' in data:
        params = data["params"]
    if 'language' in data:
        language = data["language"]

    script.update(name=name,outPutLinesNumber=outPutLinesNumber,description=description,content=content,params=params,language=language,inputs=inputs,addedBy=user)
    db.session.commit()
    return jsonify({"msg" : f'Script {script.name} succseffully updated.'}) , 200


    dicts_with_none_id = [d for d in inputs if d.get('id') is None]
    dicts_with_valid_id = [d for d in inputs if d.get('id') is not None]
    
    for input in script.inputs :
        found = False
        for newInput in dicts_with_valid_id :
            if input.id == newInput["id"] :
                found = True
                input.label = newInput["label"]
                input.type = newInput["type"]
        if found == False :
            #we have to delete if
            db.session.delete(input)
            
    
    for input in dicts_with_none_id:
        db.session.add(Inputs(label=input["label"],type=input["type"],incidentID=None,scriptID=script.id,AddedBy=user))
    
    #you have to edit inputs in step after this 
    script.content = content
    db.session.commit()
    return jsonify({"msg" :"Successfully edited"}) , 200

# ------------------------------- users routes ------------------------------- #
@app.get("/api/scripts")
@check_login
def getScripts():
    return jsonify(Scripts().listAll(content=False,query_name=request.args.get("name"))) , 200

@app.get("/api/script/<id>")
@check_login
def getScript(id):
    script = Scripts().getScriptByID(id)
    if not script:
        return jsonify({'msg' : 'Scripts does not exist.'}) , 400
    return jsonify(script.toDictionary(content=True)),200



# ---------------------------------------------------------------------------- #
#                                //Users routes                                #
# ---------------------------------------------------------------------------- #
@app.get("/api/users")
@check_login
@check_admin_privilege
def getUsers():
    return jsonify(Users().listAll(query_name=request.args.get("user"))) , 200

@app.post("/api/user/create")
@check_login
@check_admin_privilege
def createUser():
    data = request.get_json()
    username = data["username"]
    admin , execute  = None , None 

    if 'admin' in data :
        admin = data["admin"]

    if 'execute' in data :
        execute = data["execute"]    

    try :
        user = Users().create(username=username,admin=admin,execute=execute)
        db.session.commit()
        return jsonify({'msg' : f'User {username} successfully added.'}) , 200
    except Exception as e :
        return jsonify({'msg' : str(e),
                        "id" : user.id}) , 400

@app.delete("/api/user/delete")
@check_login
@check_admin_privilege
def deleteUser():
    data = request.get_json()
    id = data["id"]
    user = Users().getUserByID(id)
    if not user :
        return jsonify({"msg" : "User does not exist"}),400
    try :
        user.disableUser()
        db.session.commit()
        return jsonify({"msg" : "User successfully deleted"}),200
    except Exception as e:
        return jsonify({"msg" : str(e)}),400


# @app.get("/api/user/<id>")
# def getUser(id):
#     try :
#         id = int(id)
#     except :
#         return jsonify({"msg" : 'An error has occured.'}) , 400
#     user = Users().getUserByID(id)
#     if not user :
#         return jsonify({"msg" : 'User does not exist.'}) , 400
#     return jsonify(user.toString()), 200

@app.put("/api/user/update/execution")
@check_login
@check_admin_privilege
def updateUserExecution():
    data = request.get_json()
    id = data["id"]
    user = Users().getUserByID(id)
    if not user :
        return jsonify({"msg" : "User does not exist."}) , 400
    execution = data["execution"]
    if execution == True :
        user.enableUserExecute()
    else :
        user.disableUserExecute()
    db.session.commit()
    return jsonify({
        'msg' : f'{user.user}\'s execution hability successfully updated.',
        'id' : user.id ,
    }),200

@app.put("/api/user/activate")
@check_login
@check_admin_privilege
def activateAccount():
    data = request.get_json()
    id = data["id"]
    user = Users().getUserByID(id)
    if not user:
        return jsonify({"msg" : "User does not exist."}) , 400
    if user.account_active :
        return jsonify({'msg' : f'User {user.user} already active.'}) , 200
    else :
        user.activeUser()
        db.session.commit()
        return jsonify({'msg' : f'User {user.user} activated.',
                        "user" : user.toDictionary()}) , 200

@app.put("/api/user/admin/update")
@check_login
@check_admin_privilege
def updateAdminPrivlege():
    data = request.get_json()
    id = data["id"]
    enable = data["enable"]
    user = Users().getUserByID(id)
    if not user : 
        return jsonify({"msg" : "User does not exist."}) , 400
    if not enable :
        if not user.is_admin :
            return jsonify({'msg' : f'User {user.user} already has not admin privelege.'}) , 200
        else :
            user.DisableAdminPrivlege()
            db.session.commit()
            return jsonify({'msg' : f'User {user.user} has now his admin privelege remooved.'}) , 200
    else :
        if  user.is_admin :
            return jsonify({'msg' : f'User {user.user} already has admin privelege.'}) , 200
        else :
            user.setEnableAdminPrivlege()
            db.session.commit()
            return jsonify({'msg' : f'User {user.user} has now admin privelege.'}) , 200

@app.put("/api/user/update")
@check_login
@check_admin_privilege
def updateUser():
    data = request.get_json()
    user = data["id"]
    user = Users().getUserByID(user)
    if not user :
        return jsonify({'msg' : "User does not exsits."}) , 400

    username = data["username"]
    admin = data["admin"]
    execute = data["execute"]
    active = data["active"]


    try : 
        user.update(username=username,active=active,execute=execute,admin=admin)
        db.session.commit()
        return jsonify({'msg' : "User updated successfully."}) , 200
    except Exception as e :
        return jsonify({'msg' : str(e)}) , 400



# ---------------------------------------------------------------------------- #
#                               languages routes                               #
# ---------------------------------------------------------------------------- #
@app.get("/api/languages")
@check_login
def getLanguages():
    return [{"key": member.name, "value": member.value} for member in languages] , 200

# ---------------------------------------------------------------------------- #
#                               //to clean routes                              #
# ---------------------------------------------------------------------------- #
@app.get("/api/UAT/serverStatus/<srv>")
@check_login_UAT
def serverStatusUAT(srv):
    if srv in ExpectedServersUAT :
        response = executeCommande(ExpectedServersUAT[srv],session["AUTH_UAT"]["username"],session["AUTH_UAT"]["password"]," df -H ")
        response = "\n".join(response)
        return jsonify({"resultat" : response}) , 200
    else :
        return jsonify({"error" : "this server is not recognized"}) , 404

@app.get("/api/UAT/reachableServers/<srv>")
@check_login_UAT
def serverReachableStatus(srv):
    if srv in ExpectedServersUAT : 
        if isMyHostUp(ExpectedServersUAT[srv]):
            response={srv : True}
        else :
            response={srv : False}
        return jsonify(response) , 200
    else :
        return jsonify({"Error" : "Server not found"}) , 404


@app.get("/api/AreUUp")
@check_login
def AreUUp():
    return  jsonify({"up" : True }) , 200

@app.get("/api/Prod/serverStatus/<srv>")
@check_login_PROD
def serverStatusPROD(srv):
    if srv in ExpectedServersPROD :
        response = executeCommande(ExpectedServersPROD[srv],session["AUTH_PROD"]["username"],session["AUTH_PROD"]["password"]," df -H ")
        response = "\n".join(response)
        return jsonify({"resultat" : response}) , 200
    else :
        return jsonify({"error" : "this server is not recognized"}) , 404

