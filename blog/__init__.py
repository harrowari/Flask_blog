from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required


app = Flask(__name__)
Bootstrap(app)

app.config["SECRET_KEY"]='3dcbb92fcf85643519af1816350b07d4811c3f8e4cade554'

# SQLite database 

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir,'my_db.db')}"

# # MySQL database 

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://d1737516:Surfboard20!@csmysql.cs.cf.ac.uk:3306/d1737516_cmt120'

db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

from blog import routes
