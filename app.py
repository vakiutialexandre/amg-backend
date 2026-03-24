from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# banco
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# ------------------------
# MODELOS
# ------------------------

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
# ROTAS
# ------------------------

@app.route("/")
def home():
    return "API AMG funcionando 🚀"


# criar cliente
@app.route("/clientes", methods=["POST"])
def criar_cliente():
    data = request.json

    cliente = Cliente(
        nome=data["nome"],
        telefone=data["telefone"]
    )

    db.session.add(cliente)
    db.session.commit()

    return jsonify({"msg": "Cliente criado"})


# listar clientes
@app.route("/clientes", methods=["GET"])
def listar_clientes():
    clientes = Cliente.query.all()

    resultado = []
    for c in clientes:
        resultado.append({
            "id": c.id,
            "nome": c.nome,
            "telefone": c.telefone
        })

    return jsonify(resultado)


# criar orçamento
@app.route("/orcamentos", methods=["POST"])
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


# listar orçamentos
@app.route("/orcamentos", methods=["GET"])
def listar_orcamentos():
    orcs = Orcamento.query.all()

    resultado = []
    for o in orcs:
        resultado.append({
            "id": o.id,
            "cliente_id": o.cliente_id,
            "descricao": o.descricao,
            "valor": o.valor,
            "status": o.status
        })

    return jsonify(resultado)


# ------------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))