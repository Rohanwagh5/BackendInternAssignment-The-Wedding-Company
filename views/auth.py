# from flask import Blueprint, request, jsonify
# from flask.views import MethodView
# from flask_jwt_extended import create_access_token
# from models import get_admin_by_email, get_org_by_name
# import bcrypt

# auth_bp = Blueprint("auth", __name__, url_prefix="/admin")

# class AdminLoginAPI(MethodView):
#     def post(self):
#         data = request.get_json() or {}
#         email = data.get("email")
#         password = data.get("password")
#         if not email or not password:
#             return jsonify({"msg": "email and password required"}), 400

#         master_db = request.app.config["Organisation_DB"]
#         admin = get_admin_by_email(master_db, email)
#         if not admin:
#             return jsonify({"msg": "invalid credentials"}), 401

#         stored_hash = admin.get("password_hash").encode()
#         if not bcrypt.checkpw(password.encode(), stored_hash):
#             return jsonify({"msg": "invalid credentials"}), 401

#         # get org metadata to attach to token
#         org = get_org_by_name(master_db, admin.get("org_slug"))
#         org_id = str(org.get("_id")) if org else None

#         additional_claims = {"org_slug": admin.get("org_slug")}
#         access_token = create_access_token(identity=str(admin.get("_id")), additional_claims=additional_claims)
#         return jsonify({"access_token": access_token, "org_id": org_id}), 200

# auth_bp.add_url_rule("/login", view_func=AdminLoginAPI.as_view("admin_login"))


# views/auth.py
from flask import Blueprint, request, jsonify, current_app
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from models import get_admin_by_email, get_org_by_name
import bcrypt

auth_bp = Blueprint("auth", __name__, url_prefix="/admin")

class AdminLoginAPI(MethodView):
    def post(self):
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"msg": "email and password required"}), 400

        # <- use the canonical config key set in app.create_app()
        master_db = current_app.config["MASTER_DB"]

        admin = get_admin_by_email(master_db, email)
        if not admin:
            return jsonify({"msg": "invalid credentials"}), 401

        stored_hash = admin.get("password_hash")
        if stored_hash is None:
            return jsonify({"msg": "invalid credentials"}), 401
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode()

        if not bcrypt.checkpw(password.encode(), stored_hash):
            return jsonify({"msg": "invalid credentials"}), 401

        org_slug = admin.get("org_slug")
        additional_claims = {"org_slug": org_slug} if org_slug else {}
        access_token = create_access_token(identity=str(admin.get("_id")), additional_claims=additional_claims)

        org = get_org_by_name(master_db, org_slug) if org_slug else None
        org_id = str(org.get("_id")) if org else None

        return jsonify({"access_token": access_token, "org_id": org_id}), 200

auth_bp.add_url_rule("/login", view_func=AdminLoginAPI.as_view("admin_login"))
