
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.workflow import Workflow
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def tarefa_para_dict(tarefa):
    return {
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "status": tarefa.status,
        "workflow_id": tarefa.workflow_id,
        "created_at": (
            tarefa.created_at.isoformat()
            if tarefa.created_at else None
        )
    }


def buscar_tarefa_do_usuario(tarefa_id):
    usuario_id = int(get_jwt_identity())

    return (
        Task.query
        .join(Workflow, Task.workflow_id == Workflow.id)
        .filter(
            Task.id == tarefa_id,
            Workflow.usuario_id == usuario_id
        )
        .first()
    )


# CRIAR TAREFA
@tasks_bp.route("", methods=["POST"])
@jwt_required()
def criar_tarefa():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "JSON invalido."}), 400

    titulo = dados.get("titulo")
    workflow_id = dados.get("workflow_id")
    descricao = dados.get("descricao", "")

    if not isinstance(titulo, str) or not titulo.strip():
        return jsonify({"erro": "Titulo obrigatorio."}), 400

    if type(workflow_id) is not int:
        return jsonify({"erro": "workflow_id invalido."}), 400

    if descricao is not None and not isinstance(descricao, str):
        return jsonify({"erro": "Descricao invalida."}), 400

    workflow = Workflow.query.filter_by(
        id=workflow_id,
        usuario_id=int(get_jwt_identity())
    ).first()

    if not workflow:
        return jsonify({"erro": "Workflow nao encontrado."}), 404

    tarefa = Task(
        titulo=titulo.strip(),
        descricao=descricao,
        workflow_id=workflow.id
    )

    db.session.add(tarefa)
    db.session.commit()

    return jsonify(tarefa_para_dict(tarefa)), 201


# LISTAR TAREFAS
@tasks_bp.route("", methods=["GET"])
@jwt_required()
def listar_tarefas():
    usuario_id = int(get_jwt_identity())

    tarefas = (
        Task.query
        .join(Workflow, Task.workflow_id == Workflow.id)
        .filter(Workflow.usuario_id == usuario_id)
        .order_by(Task.id.desc())
        .all()
    )

    return jsonify([
        tarefa_para_dict(tarefa) for tarefa in tarefas
    ]), 200


# CONSULTAR TAREFA
@tasks_bp.route("/<int:tarefa_id>", methods=["GET"])
@jwt_required()
def consultar_tarefa(tarefa_id):
    tarefa = buscar_tarefa_do_usuario(tarefa_id)

    if not tarefa:
        return jsonify({"erro": "Tarefa nao encontrada."}), 404

    return jsonify(tarefa_para_dict(tarefa)), 200


# ATUALIZAR TAREFA
@tasks_bp.route("/<int:tarefa_id>", methods=["PUT"])
@jwt_required()
def atualizar_tarefa(tarefa_id):
    tarefa = buscar_tarefa_do_usuario(tarefa_id)

    if not tarefa:
        return jsonify({"erro": "Tarefa nao encontrada."}), 404

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "JSON invalido."}), 400

    if "titulo" in dados:
        titulo = dados["titulo"]

        if not isinstance(titulo, str) or not titulo.strip():
            return jsonify({"erro": "Titulo invalido."}), 400

        tarefa.titulo = titulo.strip()

    if "descricao" in dados:
        descricao = dados["descricao"]

        if descricao is not None and not isinstance(descricao, str):
            return jsonify({"erro": "Descricao invalida."}), 400

        tarefa.descricao = descricao

    if "status" in dados:
        status = dados["status"]

        if not isinstance(status, str) or not status.strip():
            return jsonify({"erro": "Status invalido."}), 400

        tarefa.status = status.strip()

    if "workflow_id" in dados:
        workflow_id = dados["workflow_id"]

        if type(workflow_id) is not int:
            return jsonify({"erro": "workflow_id invalido."}), 400

        workflow = Workflow.query.filter_by(
            id=workflow_id,
            usuario_id=int(get_jwt_identity())
        ).first()

        if not workflow:
            return jsonify({"erro": "Workflow nao encontrado."}), 404

        tarefa.workflow_id = workflow.id

    db.session.commit()

    return jsonify(tarefa_para_dict(tarefa)), 200


# EXCLUIR TAREFA
@tasks_bp.route("/<int:tarefa_id>", methods=["DELETE"])
@jwt_required()
def excluir_tarefa(tarefa_id):
    tarefa = buscar_tarefa_do_usuario(tarefa_id)

    if not tarefa:
        return jsonify({"erro": "Tarefa nao encontrada."}), 404

    db.session.delete(tarefa)
    db.session.commit()

    return jsonify({
        "mensagem": "Tarefa excluida com sucesso."
    }), 200
