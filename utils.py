from pymongo.errors import CollectionInvalid
from bson.objectid import ObjectId

def slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "_")

def create_collection_if_not_exists(db, collection_name: str):
    if collection_name in db.list_collection_names():
        return db[collection_name]
    try:
        return db.create_collection(collection_name)
    except CollectionInvalid:
        return db[collection_name]

def copy_collection(db, src_name: str, dst_name: str, batch_size=100):
    """
    Copy all documents from src collection to dst collection.
    Keeps original docs except _id (new _id will be created).
    """
    src = db[src_name]
    dst = create_collection_if_not_exists(db, dst_name)
    cursor = src.find({})
    batch = []
    for doc in cursor:
        doc.pop("_id", None)
        batch.append(doc)
        if len(batch) >= batch_size:
            dst.insert_many(batch)
            batch = []
    if batch:
        dst.insert_many(batch)
