from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

login= LoginManager()

from .review.routes import reviews
from .review.routes import shelf
from .auth.routes import auth
from .models import User


app = Flask(__name__)
CORS(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.config.from_object(Config)
app.register_blueprint(auth)
app.register_blueprint(reviews)
app.register_blueprint(shelf)


from .models import db 

db.init_app(app)
migrate = Migrate(app,db)
login.init_app(app)

login.login_view = 'auth.logMeIn'

from . import routes
from . import models