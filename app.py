from flask import Flask, g
from config import Config
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
import os

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = Config.JWT_ACCESS_TOKEN_EXPIRES

    client = MongoClient(Config.MONGO_URI)
    master_db = client[Config.MASTER_DB]
    app.config["MONGO_CLIENT"] = client
    app.config["MASTER_DB"] = master_db

    jwt = JWTManager(app)

    from views.orgs import org_bp
    from views.auth import auth_bp
    app.register_blueprint(org_bp)
    app.register_blueprint(auth_bp)

    SWAGGER_URL = "/docs"                 
    API_URL = "/static/openapi.json"      
    swagger_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={ "app_name": "Organization Management API" }
    )
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    @app.route("/")
    def health():
        return {"status": "ok", "service": "organization-management"}, 200

    return app
