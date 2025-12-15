import firebase_admin
from firebase_admin import credentials, auth, firestore
import os

# Caminho do JSON (Render aceita se estiver no repo)
FIREBASE_JSON_PATH = os.path.join(os.path.dirname(__file__), "firebase_key.json")

# Inicializa o Firebase UMA ÚNICA VEZ
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_JSON_PATH)
    firebase_admin.initialize_app(cred)

# Serviços exportados
db = firestore.client()
