from flask import Blueprint, request, jsonify, current_app
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from models import org_exists, create_admin, get_org_by_name
from utils import slugify, create_collection_if_not_exists, copy_collection
import bcrypt
from datetime import datetime
from bson.objectid import ObjectId

org_bp = Blueprint("orgs", __name__, url_prefix="/org")

class OrgCreateAPI(MethodView):
    def post(self):
        data = request.get_json() or {}
        org_name = data.get("organization_name")
        admin_email = data.get("email")
        admin_password = data.get("password")

        if not org_name or not admin_email or not admin_password:
            return jsonify({"msg": "organization_name, email, password required"}), 400

        master_db = current_app.config["MASTER_DB"]
        org_slug = slugify(org_name)
        if org_exists(master_db, org_slug):
            return jsonify({"msg": "organization already exists"}), 409

        collection_name = f"org_{org_slug}"
        create_collection_if_not_exists(master_db, collection_name)

        pw_hash = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt())
        admin_id = create_admin(master_db, admin_email, pw_hash.decode(), org_slug)

        org_doc = {
            "org_name": org_name,
            "org_slug": org_slug,
            "collection_name": collection_name,
            "admin_ref": admin_id,
            "created_at": datetime.utcnow(),
        }
        res = master_db.organizations.insert_one(org_doc)
        org_doc["_id"] = str(res.inserted_id)
        return jsonify({"msg": "organization created", "organization": {"org_name": org_name, "collection_name": collection_name}}), 201

class OrgGetAPI(MethodView):
    def get(self):
        org_name = request.args.get("organization_name")
        if not org_name:
            return jsonify({"msg": "organization_name query param required"}), 400
        org_slug = slugify(org_name)
        master_db = current_app.config["MASTER_DB"]
        org = get_org_by_name(master_db, org_slug)
        if not org:
            return jsonify({"msg": "organization not found"}), 404
        
        org["_id"] = str(org["_id"])
        return jsonify({"organization": {"org_name": org["org_name"], "collection_name": org["collection_name"], "created_at": org.get("created_at")}}), 200

class OrgUpdateAPI(MethodView):
    def put(self):
        data = request.get_json() or {}
        org_name = data.get("organization_name")
        new_name = data.get("new_organization_name")  
        new_email = data.get("email")   
        new_password = data.get("password") 

        if not org_name:
            return jsonify({"msg": "organization_name required"}), 400

        master_db = current_app.config["MASTER_DB"]
        org_slug = slugify(org_name)
        org = get_org_by_name(master_db, org_slug)
        if not org:
            return jsonify({"msg": "organization not found"}), 404

        update_fields = {}
        if new_name:
            new_slug = slugify(new_name)
            if org_exists(master_db, new_slug):
                return jsonify({"msg": "new organization name already exists"}), 409
            old_collection = org["collection_name"]
            new_collection = f"org_{new_slug}"
            create_collection_if_not_exists(master_db, new_collection)
            copy_collection(master_db, old_collection, new_collection)
            update_fields["org_name"] = new_name
            update_fields["org_slug"] = new_slug
            update_fields["collection_name"] = new_collection

        if new_email or new_password:
            admin_id = org.get("admin_ref")
            if admin_id:
                admins_coll = master_db.admins
                updates = {}
                if new_email:
                    updates["email"] = new_email
                if new_password:
                    pw_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                    updates["password_hash"] = pw_hash
                if updates:
                    admins_coll.update_one({"_id": admin_id}, {"$set": updates})

        if update_fields:
            master_db.organizations.update_one({"_id": org["_id"]}, {"$set": update_fields})

        return jsonify({"msg": "organization updated"}), 200

class OrgDeleteAPI(MethodView):
    @jwt_required()
    def delete(self):
        data = request.get_json() or {}
        org_name = data.get("organization_name")
        if not org_name:
            return jsonify({"msg": "organization_name required"}), 400

        master_db = current_app.config["MASTER_DB"]
        org_slug = slugify(org_name)
        org = get_org_by_name(master_db, org_slug)
        if not org:
            return jsonify({"msg": "organization not found"}), 404

      
        jwt_claims = get_jwt()
        token_org_slug = jwt_claims.get("org_slug")
        if token_org_slug != org_slug:
            return jsonify({"msg": "forbidden: only admin of this organization can delete"}), 403

        collection_name = org["collection_name"]
        if collection_name in master_db.list_collection_names():
            master_db.drop_collection(collection_name)

        admin_ref = org.get("admin_ref")
        if admin_ref:
            master_db.admins.delete_one({"_id": admin_ref})

        master_db.organizations.delete_one({"_id": org["_id"]})
        return jsonify({"msg": "organization and its collection deleted"}), 200

org_bp.add_url_rule("/create", view_func=OrgCreateAPI.as_view("org_create"))
org_bp.add_url_rule("/get", view_func=OrgGetAPI.as_view("org_get"))
org_bp.add_url_rule("/update", view_func=OrgUpdateAPI.as_view("org_update"))
org_bp.add_url_rule("/delete", view_func=OrgDeleteAPI.as_view("org_delete"))
