
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.workflow import Workflow

workflows_bp = Blueprint(
    "workflows",
    __name__,
    url_prefix="/workflows"
)


def workflow_para_dict(workflow):
    return {
        "id": workflow.id,
        "nome": workflow.nome,
        "descricao": workflow.descricao,
        "status": workflow.status,
        "usuario_id": workflow.usuario_id,
        "created_at": (
            workflow.created_at.isoformat()
            if workflow.created_at else None
        )
    }


# CRIAR WORKFLOW
@workflows_bp.route("", methods=["POST"])
@jwt_required()
def criar_workflow():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "JSON invalido."}), 400

    nome = dados.get("nome")
    descricao = dados.get("descricao", "")

    if not isinstance(nome, str) or not nome.strip():
        return jsonify({"erro": "O nome e obrigatorio."}), 400

    if descricao is not None and not isinstance(descricao, str):
        return jsonify({"erro": "Descricao invalida."}), 400

    workflow = Workflow(
        nome=nome.strip(),
        descricao=descricao,
        usuario_id=int(get_jwt_identity())
    )

    db.session.add(workflow)
    db.session.commit()

    return jsonify(workflow_para_dict(workflow)), 201


# LISTAR WORKFLOWS
@workflows_bp.route("", methods=["GET"])
@jwt_required()
def listar_workflows():
    usuario_id = int(get_jwt_identity())

    workflows = Workflow.query.filter_by(
        usuario_id=usuario_id
    ).order_by(Workflow.id.desc()).all()

    return jsonify([
        workflow_para_dict(workflow)
        for workflow in workflows
    ]), 200


# CONSULTAR WORKFLOW POR ID
@workflows_bp.route("/<int:workflow_id>", methods=["GET"])
@jwt_required()
def consultar_workflow(workflow_id):
    usuario_id = int(get_jwt_identity())

    workflow = Workflow.query.filter_by(
        id=workflow_id,
        usuario_id=usuario_id
    ).first()

    if not workflow:
        return jsonify({"erro": "Workflow nao encontrado."}), 404

    return jsonify(workflow_para_dict(workflow)), 200


# ATUALIZAR WORKFLOW
@workflows_bp.route("/<int:workflow_id>", methods=["PUT"])
@jwt_required()
def atualizar_workflow(workflow_id):
    usuario_id = int(get_jwt_identity())

    workflow = Workflow.query.filter_by(
        id=workflow_id,
        usuario_id=usuario_id
    ).first()

    if not workflow:
        return jsonify({"erro": "Workflow nao encontrado."}), 404

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "JSON invalido."}), 400

    if "nome" in dados:
        nome = dados["nome"]

        if not isinstance(nome, str) or not nome.strip():
            return jsonify({"erro": "Nome invalido."}), 400

        workflow.nome = nome.strip()

    if "descricao" in dados:
        descricao = dados["descricao"]

        if descricao is not None and not isinstance(descricao, str):
            return jsonify({"erro": "Descricao invalida."}), 400

        workflow.descricao = descricao

    if "status" in dados:
        status = dados["status"]

        if not isinstance(status, str) or not status.strip():
            return jsonify({"erro": "Status invalido."}), 400

        workflow.status = status.strip()

    db.session.commit()

    return jsonify(workflow_para_dict(workflow)), 200


# EXCLUIR WORKFLOW
@workflows_bp.route("/<int:workflow_id>", methods=["DELETE"])
@jwt_required()
def excluir_workflow(workflow_id):
    usuario_id = int(get_jwt_identity())

    workflow = Workflow.query.filter_by(
        id=workflow_id,
        usuario_id=usuario_id
    ).first()

    if not workflow:
        return jsonify({"erro": "Workflow nao encontrado."}), 404

    db.session.delete(workflow)
    db.session.commit()

    return jsonify({
        "mensagem": "Workflow excluido com sucesso."
    }), 200
