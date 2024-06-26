import firebase_admin
import dotenv, os
from firebase_admin import credentials, firestore, initialize_app, storage
from misc_helper import load_firebase_credentials

def init_firebase_app(env_file):
    dotenv.load_dotenv(dotenv_path=env_file)

    # Initialize the configs for the Firebase Admin SDK
    firebase_config = {}
    firebase_config['apiKey'] = os.getenv('firebase_apiKey')[1:-1]
    firebase_config['authDomain'] = os.getenv('firebase_authDomain')[1:-1]
    firebase_config['projectId'] = os.getenv('firebase_projectId')[1:-1]
    firebase_config['storageBucket'] = os.getenv('firebase_storageBucket')[1:-1]
    firebase_config['messagingSenderId'] = os.getenv('firebase_messagingSenderId')[1:-1]
    firebase_config['appId'] = os.getenv('firebase_appId')[1:-1]
    firebase_config['measurementId'] = os.getenv('firebase_measurementId')[1:-1]
    firebase_config['serviceAccount'] = "firestore-credentials.json"

    cred_json = load_firebase_credentials(env_file)
    print(cred_json)
    
    cred = credentials.Certificate(cred_json)

    app = firebase_admin.initialize_app(credential=cred, options=firebase_config)
    
    return app

def init_firestore(env_file, app = None):
    if app is None:
        app = init_firebase_app(env_file)
    db = firestore.client(app)
    return db

def init_storage(env_file, app = None):
    if app is None:
        app = init_firebase_app(env_file)
        print("App type: ", type(app))
    storage_instance = storage.bucket(name="bangkit-capstone-dms.appspot.com", app=app)
    return storage_instance

def add_data(collection_name, data, db = None):
    if db is None:
        db = init_firestore('.env')
    # Add a new document with a generated ID
    db.collection(collection_name).add(data)
    print("Document added successfully")

def add_driver_video(bytes, driver_id, timestamp, storage = None):
    if storage is None:
        print("Storage initialized")
        storage = init_storage('.env')
    print(type(storage))
    try:
        filename = str(driver_id + "_" + timestamp + ".avi")
        destination_blob_path = "frames/" + filename
        blob = storage.blob(destination_blob_path)
        blob.upload_from_string(bytes, content_type='video/avi')
        blob.make_public()
        print("File added successfully")
        return blob.public_url
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Frame not added successfully"}

def get_data_from_firestore(collection, doc_id, db = None):
    if db is None:
        db = init_firestore('.env')
    doc_ref = db.collection(collection).document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {"message": "No such document!"}
    
def get_collection_data(collection, db=None):
  if db is None:
    db = init_firestore('.env')
  collection_ref = db.collection_group(collection)
  # Get all documents in the collection
  docs = collection_ref.get()

  try:
    # Get data as dictionaries from each document snapshot
    return [doc.to_dict() for doc in docs if doc.exists]
  except Exception as e:
    raise Exception(f"Error getting collection data: {e}")