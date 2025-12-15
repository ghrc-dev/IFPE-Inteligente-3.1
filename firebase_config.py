import os
import json
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Carrega o JSON da variável de ambiente
firebase_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

# Corrige a chave privada para ter quebras de linha reais
private_key = firebase_json["private_key"]
private_key = private_key.replace("\\n", "\n")
firebase_json["private_key"] = private_key

# Inicializa o Firebase
cred = credentials.Certificate(firebase_json)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
