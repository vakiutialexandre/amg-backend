from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
import os

app = Flask(__name__)

# CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["JWT_SECRET_KEY"] = "super-secret-key"

db = SQLAlchemy(app)
jwt = JWTManager(app)

# ------------------------
# MODELOS
# ------------------------

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(20))


class Orcamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer)
    descricao = db.Column(db.String(200))
    valor = db.Column(db.Float)
    status = db.Column(db.String(50))


# ------------------------
# AUTH
# ------------------------

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    user = Usuario(
        username=data["username"],
        senha=data["senha"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Usuário criado"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = Usuario.query.filter_by(username=data["username"]).first()

    if not user or user.senha != data["senha"]:
        return jsonify({"msg": "Credenciais inválidas"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"token": token})


# ------------------------
# CLIENTES
# ------------------------

@app.route("/clientes", methods=["POST"])
@jwt_required()
def criar_cliente():
    data = request.json

    cliente = Cliente(
        nome=data["nome"],
        telefone=data["telefone"]
    )

    db.session.add(cliente)
    db.session.commit()

    return jsonify({"msg": "Cliente criado"})


@app.route("/clientes", methods=["GET"])
@jwt_required()
def listar_clientes():
    clientes = Cliente.query.all()

    return jsonify([
        {"id": c.id, "nome": c.nome, "telefone": c.telefone}
        for c in clientes
    ])


@app.route("/clientes/<int:id>", methods=["PUT"])
@jwt_required()
def editar_cliente(id):
    cliente = Cliente.query.get(id)
    data = request.json

    cliente.nome = data["nome"]
    cliente.telefone = data["telefone"]

    db.session.commit()

    return jsonify({"msg": "Atualizado"})


@app.route("/clientes/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar_cliente(id):
    cliente = Cliente.query.get(id)

    db.session.delete(cliente)
    db.session.commit()

    return jsonify({"msg": "Deletado"})


# ------------------------
# ORÇAMENTOS
# ------------------------

@app.route("/orcamentos", methods=["POST"])
@jwt_required()
def criar_orcamento():
    data = request.json

    orc = Orcamento(
        cliente_id=data["cliente_id"],
        descricao=data["descricao"],
        valor=data["valor"],
        status="pendente"
    )

    db.session.add(orc)
    db.session.commit()

    return jsonify({"msg": "Orçamento criado"})


@app.route("/orcamentos", methods=["GET"])
@jwt_required()
def listar_orcamentos():
    orcs = Orcamento.query.all()

    return jsonify([
        {
            "id": o.id,
            "cliente_id": o.cliente_id,
            "descricao": o.descricao,
            "valor": o.valor,
            "status": o.status
        }
        for o in orcs
    ])


@app.route("/orcamentos/<int:id>/status", methods=["PUT"])
@jwt_required()
def atualizar_status(id):
    orc = Orcamento.query.get(id)
    data = request.json

    orc.status = data["status"]
    db.session.commit()

    return jsonify({"msg": "Status atualizado"})


# ------------------------

@app.route("/")
def home():
    return "API AMG FULL SYSTEM 🚀"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))