from flask import Flask 
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import timedelta
import logging

from .LDAP.auth import ldap_conn

app = Flask(__name__)

app.config['SECRET_KEY'] = "esfdfsgsfdsggdfsfdfsd"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_SAMESITE'] = None

app.config['SESSION_COOKIE_SECURE'] = False
# app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_DURATION'] = timedelta(minutes=60)

app.config['SESSION_COOKIE_DOMAIN'] = '192.168.1.52'




# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='BanxyICDDB.2023', server='localhost', database='banxyincidentsdb')
#My lOCAL MAC MYSQL app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='madjid123', server='127.0.0.1', database='banxyincidentsdb')
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='madjid123', server='192.168.1.52:3366', database='banxyincidentsdb')

app.config["LDAP_SERVER"] ="ldap://192.168.1.65:389"
app.config["ROOT_DN"] = "dc=jidsu-company,dc=com"
app.config["LDAP_BIND_USERNAME"] = "admin"
app.config["LDAP_BIND_PASSWORD"] = "admin"

app.config['USER_APP'] = 'userapp'
app.config['USER_APP_PASSWORD'] = 'userapp'


app.logger.setLevel(logging.INFO)  # Set log level to INFO
handler = logging.FileHandler('app.log')  # Log to a file
app.logger.addHandler(handler)

db = SQLAlchemy(app)

session_server = Session(app)

CORS(app,supports_credentials=True)

ldap = ldap_conn(app)

DOMAIN = ""

''' session["AUTH"] = { 
    "username" : username,
    "Password" : password,
}'''  
# list_srv_UAT = ["192.168.1.69"] 
ExpectedServersUAT = {}
ExpectedServersPROD = {}

from main import routes ,Command


# Command.innitServerDictionarry()