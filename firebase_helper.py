import firebase_admin
import dotenv, os
from firebase_admin import credentials, firestore, initialize_app
from misc_helper import load_firebase_credentials

def init_firestore(env_file):
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

    cred_json = load_firebase_credentials(env_file)
    print(cred_json)
    
    cred = credentials.Certificate(cred_json)

    app = firebase_admin.initialize_app(credential=cred, options=firebase_config)

    db = firestore.client(app)
    
    return db

def add_data(collection_name, data ,db = None):
    if db is None:
        db = init_firestore('.env')
    # Add a new document with a generated ID
    db.collection(collection_name).add(data)
    print("Document added successfully")