from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.user import User

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "JSON inválido."}), 400

    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    if not nome or not email or not senha:
        return jsonify({
            "erro": "Nome, email e senha são obrigatórios."
        }), 400

    usuario_existente = User.query.filter_by(email=email).first()

    if usuario_existente:
        return jsonify({
            "erro": "E-mail já cadastrado."
        }), 409

    senha_hash = generate_password_hash(senha)

    novo_usuario = User(
        nome=nome,
        email=email,
        senha=senha_hash
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({
        "id": novo_usuario.id,
        "nome": novo_usuario.nome,
        "email": novo_usuario.email
    }), 201