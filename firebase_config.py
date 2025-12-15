import os
import json
import firebase_admin
from firebase_admin import credentials, auth, firestore

firebase_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

# 🔥 CORREÇÃO CRÍTICA
firebase_json["private_key"] = firebase_json["private_key"].replace("\\n", "\n")

cred = credentials.Certificate(firebase_json)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
