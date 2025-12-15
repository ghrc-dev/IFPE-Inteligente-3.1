from flask import Flask, render_template, request, redirect, session, jsonify
from firebase_config import auth, db
import requests
import os
from google.cloud import firestore

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ifpe-inteligente")

API_KEY = os.environ.get("FIREBASE_API_KEY")


# ========= LOGIN FIREBASE =========
def login_firebase(email, senha):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {
        "email": email,
        "password": senha,
        "returnSecureToken": True
    }

    try:
        r = requests.post(url, json=payload, timeout=8)
        return r.json()
    except Exception as e:
        print("ERRO LOGIN FIREBASE:", e)
        return {}


# ========= TELA INICIAL =========
@app.route("/")
def index():
    return render_template("telainicial.html")


# ========= CRIAR CONTA =========
@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    if request.method == "POST":
        try:
            user = auth.create_user(
                email=request.form["email"],
                password=request.form["senha"],
                display_name=request.form["nome"]
            )

            db.collection("usuarios").document(user.uid).set({
                "nome": request.form["nome"],
                "email": request.form["email"],
                "curso": request.form["curso"],
                "turma": request.form["serie"],
                "pontos": 0,
                "locais_visitados": []
            })

            return redirect("/login")

        except Exception as e:
            print("ERRO CRIAR CONTA:", e)
            return "Erro ao criar conta"

    return render_template("criarconta.html")


# ========= LOGIN =========
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        resultado = login_firebase(
            request.form["email"],
            request.form["senha"]
        )

        if "localId" in resultado:
            session.clear()
            session["user"] = resultado["localId"]
            return redirect("/home")

        return "Email ou senha incorretos"

    return render_template("telalogin.html")


# ========= HOME =========
@app.route("/home")
def home():
    if "user" not in session or not session["user"]:
        session.clear()
        return redirect("/login")

    try:
        ref = db.collection("usuarios").document(session["user"])
        doc = ref.get()

        if not doc.exists:
            session.clear()
            return redirect("/login")

        usuario = doc.to_dict()

    except Exception as e:
        print("ERRO HOME:", e)
        session.clear()
        return redirect("/login")

    return render_template("home.html", usuario=usuario)


# ========= PERFIL =========
@app.route("/perfil")
def perfil():
    if "user" not in session or not session["user"]:
        session.clear()
        return redirect("/login")

    try:
        doc = db.collection("usuarios").document(session["user"]).get()
        usuario = doc.to_dict() if doc.exists else {}
    except Exception as e:
        print("ERRO PERFIL:", e)
        session.clear()
        return redirect("/login")

    return render_template("perfil.html", usuario=usuario)


# ========= CONFIG =========
@app.route("/config")
def configuracoes():
    if "user" not in session:
        return redirect("/login")
    return render_template("configuracoes.html")


# ========= IFPE FLOW =========
@app.route("/ifpeflow")
def ifpeflow():
    if "user" not in session:
        return redirect("/login")
    return render_template("ifpeflow.html")


# ========= ECOSCAN =========
@app.route("/ecoscan")
def ecoscan():
    if "user" not in session:
        return redirect("/login")
    return render_template("ecoscan.html")


# ========= HELPME =========
@app.route("/helpme")
def helpme():
    if "user" not in session or not session["user"]:
        session.clear()
        return redirect("/login")

    try:
        doc = db.collection("usuarios").document(session["user"]).get()
        usuario = doc.to_dict() if doc.exists else {}
    except Exception as e:
        print("ERRO HELPME:", e)
        session.clear()
        return redirect("/login")

    return render_template("helpme.html", usuario=usuario)


# ========= REGISTRAR LIXO =========
@app.route("/registrar_lixo", methods=["POST"])
def registrar_lixo():
    if "user" not in session:
        return jsonify({"erro": "não logado"}), 403

    dados = request.get_json() or {}
    quantidade = int(dados.get("quantidade", 0))

    ref = db.collection("usuarios").document(session["user"])
    user_data = ref.get().to_dict() or {}

    novo_total = user_data.get("pontos", 0) + quantidade
    ref.update({"pontos": novo_total})

    return jsonify({
        "status": "ok",
        "pontos_adicionados": quantidade,
        "novo_total": novo_total
    })


# ========= RANKING =========
@app.route("/ranking")
def ranking():
    user_id = session.get("user")

    usuarios = (
        db.collection("usuarios")
        .order_by("pontos", direction=firestore.Query.DESCENDING)
        .limit(5)
        .stream()
    )

    ranking = []
    for doc in usuarios:
        data = doc.to_dict()
        ranking.append({
            "id": doc.id,
            "nome": data.get("nome", "Sem nome"),
            "pontos": data.get("pontos", 0),
            "is_me": doc.id == user_id
        })

    return jsonify({"ranking": ranking})


# ========= EDITAR PERFIL =========
@app.route("/editarperfil")
def editarperfil():
    if "user" not in session:
        return redirect("/login")
    return render_template("editarperfil.html")


# ========= LOGOUT =========
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

