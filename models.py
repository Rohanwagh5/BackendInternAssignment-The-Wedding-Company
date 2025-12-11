from bson.objectid import ObjectId
from datetime import datetime

def org_exists(master_db, org_name_slug):
    return master_db.organizations.find_one({"org_slug": org_name_slug}) is not None

def get_org_by_name(master_db, org_name_slug):
    return master_db.organizations.find_one({"org_slug": org_name_slug})

def create_admin(master_db, email, password_hash, org_slug):
    admin_doc = {
        "email": email,
        "password_hash": password_hash,
        "org_slug": org_slug,
        "created_at": datetime.now(),
    }
    res = master_db.admins.insert_one(admin_doc)
    return res.inserted_id

def get_admin_by_email(master_db, email):
    return master_db.admins.find_one({"email": email})


