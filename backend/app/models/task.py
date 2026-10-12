from datetime import datetime
from app.extensions import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(
        db.String(150),
        nullable=False
    )

    descricao = db.Column(db.Text)

    status = db.Column(
        db.String(50),
        default="A Fazer"
    )

    workflow_id = db.Column(
        db.Integer,
        db.ForeignKey("workflows.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Task {self.titulo}>"