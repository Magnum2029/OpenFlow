from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():

    usuario_id = int(get_jwt_identity())

    usuario = User.query.get(usuario_id)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email
    }), 200