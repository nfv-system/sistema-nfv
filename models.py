from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Campania(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)


class Lote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    superficie = db.Column(db.Float)
    cultivo = db.Column(db.String(100))

    campania_id = db.Column(db.Integer, db.ForeignKey('campania.id'))


class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.Date, nullable=False)
    tipo_labor = db.Column(db.String(100))
    detalle = db.Column(db.Text)
    dosis = db.Column(db.String(100))
    maquinaria = db.Column(db.String(100))
    operario = db.Column(db.String(100))
    observaciones = db.Column(db.Text)

    lote_id = db.Column(db.Integer, db.ForeignKey('lote.id'))