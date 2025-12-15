import os
import json
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Carrega credencial via variável de ambiente
firebase_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

cred = credentials.Certificate(firebase_json)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
