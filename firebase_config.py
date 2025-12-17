import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, auth

firebase_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

# 🔥 ESSENCIAL: corrigir quebras de linha
firebase_json["private_key"] = firebase_json["private_key"].replace("\\n", "\n")

cred = credentials.Certificate(firebase_json)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
