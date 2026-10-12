from flask import Flask

from app.config import Config
from app.extensions import db, jwt, cors, ma
from app.routes.tasks import tasks_bp

# Rotas
from app.routes.users import users_bp
from app.routes.auth import auth_bp
from app.routes.profile import profile_bp

# Modelos
from app.models.user import User
from app.models.workflow import Workflow
from app.models.task import Task
from app.routes.workflows import workflows_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    ma.init_app(app)

    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(workflows_bp)
    app.register_blueprint(tasks_bp)
    @app.route("/")
    def home():
        return {
            "message": "OpenFlow API",
            "status": "online"
        }

    with app.app_context():
        db.create_all()

    return app