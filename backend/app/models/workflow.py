from datetime import datetime
from app.extensions import db


class Workflow(db.Model):
    __tablename__ = "workflows"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150), nullable=False)

    descricao = db.Column(db.Text)

    status = db.Column(
        db.String(50),
        default="Pendente"
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    tarefas = db.relationship(
        "Task",
        backref="workflow",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Workflow {self.nome}>"