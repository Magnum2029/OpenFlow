from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():

    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400

    email = dados.get("email")
    senha = dados.get("senha")

    usuario = User.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    if not check_password_hash(usuario.senha, senha):
        return jsonify({"erro": "Senha incorreta."}), 401

    token = create_access_token(identity=str(usuario.id))

    return jsonify({
        "access_token": token,
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        }
    }), 200