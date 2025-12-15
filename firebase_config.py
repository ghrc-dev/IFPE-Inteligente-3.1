import os
import json
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Lê o JSON do Firebase pelas variáveis de ambiente
firebase_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

# Corrige quebra de linha da private_key
firebase_json["private_key"] = firebase_json["private_key"].replace("\\n", "\n")

# Inicializa o Firebase UMA ÚNICA VEZ
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_json)
    firebase_admin.initialize_app(cred)

# Exporta serviços
db = firestore.client()
