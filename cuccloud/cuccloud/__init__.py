#-*- encoding=UTF-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import and_,or_
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone

app = Flask(__name__)
bootstrap = Bootstrap(app)
dropzone = Dropzone(app)

app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile('app.conf')
app.secret_key = 'cuc'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = '/login/'

from cuccloud import views, models


