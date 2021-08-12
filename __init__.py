from flask import Flask
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import jsonify


app = Flask(__name__)

app.config['SECRET_KEY']='231a23f784d2b30a8e5f45665c3ac8d1'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

app.config['DEBUG']=True

app.config['TESTING']=False

app.config['MAIL_SERVER']='smtp.gmail.com'

app.config['MAIL_PORT']=587

app.config['MAIL_USE_TLS']=True

app.config['MAIL_USE_SSL']=	False

app.config['MAIL_DEBUG']=True

app.config['MAIL_USERNAME']='panaceadispensary2020@gmail.com'

app.config['MAIL_PASSWORD']='sanuanshiprakriti'

app.config['MAIL_DEFAULT_SENDER']='panaceadispensary2020@gmail.com'

app.config['MAIL_MAX_EMAILS']=None

app.config['MAIL_SUPPRESS_SEND']=False

app.config['MAIL_ASCII_ATTACHMENTS']=False


db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
mail=Mail(app)
login_manager.login_view='homepage'
login_manager.login_message_category='info'

from connector import routes