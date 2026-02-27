print("Arrancando SISTEMA NFV...")

from flask import Flask, render_template, request, redirect, url_for
from models import db, Campania, Lote, Tarea
from datetime import datetime

app = Flask(__name__)

import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'nfv_super_secret_key'

db.init_app(app)

with app.app_context():
    db.create_all()


# 🏠 HOME
@app.route("/")
def home():
    return render_template("home.html")


# ➕ CREAR CAMPAÑA
@app.route("/crear_campania", methods=["GET", "POST"])
def crear_campania():

    if request.method == "POST":
        nombre = request.form["nombre"]
        fecha_inicio = request.form["fecha_inicio"]
        fecha_fin = request.form["fecha_fin"]

        nueva_campania = Campania(
            nombre=nombre,
            fecha_inicio=datetime.strptime(fecha_inicio, "%Y-%m-%d"),
            fecha_fin=datetime.strptime(fecha_fin, "%Y-%m-%d")
        )

        db.session.add(nueva_campania)
        db.session.commit()

        return redirect(url_for("ver_campanias"))

    return render_template("crear_campania.html")


# 📜 VER CAMPAÑAS
@app.route("/campanias")
def ver_campanias():
    campanias = Campania.query.all()
    return render_template("ver_campanias.html", campanias=campanias)


# 🌱 CREAR LOTE
@app.route("/crear_lote/<int:campania_id>", methods=["GET", "POST"])
def crear_lote(campania_id):

    if request.method == "POST":
        nombre = request.form["nombre"]
        superficie = request.form["superficie"]
        cultivo = request.form["cultivo"]

        nuevo_lote = Lote(
            nombre=nombre,
            superficie=superficie,
            cultivo=cultivo,
            campania_id=campania_id
        )

        db.session.add(nuevo_lote)
        db.session.commit()

        return redirect(url_for("ver_lotes", campania_id=campania_id))

    return render_template("crear_lote.html", campania_id=campania_id)


# 📋 VER LOTES
@app.route("/lotes/<int:campania_id>")
def ver_lotes(campania_id):
    lotes = Lote.query.filter_by(campania_id=campania_id).all()
    return render_template("ver_lotes.html", lotes=lotes, campania_id=campania_id)


# 📋 CARGAR TAREA POR LOTE
@app.route("/cargar_tarea/<int:lote_id>", methods=["GET", "POST"])
def cargar_tarea(lote_id):

    if request.method == "POST":
        fecha = request.form["fecha"]
        tipo_labor = request.form["tipo_labor"]
        detalle = request.form["detalle"]
        dosis = request.form["dosis"]
        maquinaria = request.form["maquinaria"]
        operario = request.form["operario"]
        observaciones = request.form["observaciones"]

        nueva_tarea = Tarea(
            fecha=datetime.strptime(fecha, "%Y-%m-%d"),
            tipo_labor=tipo_labor,
            detalle=detalle,
            dosis=dosis,
            maquinaria=maquinaria,
            operario=operario,
            observaciones=observaciones,
            lote_id=lote_id
        )

        db.session.add(nueva_tarea)
        db.session.commit()

        return redirect(url_for("ver_lotes", campania_id=1))

    return render_template("cargar_tarea.html", lote_id=lote_id)

# 📜 HISTORIAL DE UN LOTE
# 📜 HISTORIAL DE UN LOTE
@app.route("/historial/<int:lote_id>")
def historial_lote(lote_id):
    tareas = Tarea.query.filter_by(lote_id=lote_id)\
                         .order_by(Tarea.fecha.asc())\
                         .all()

    return render_template("historial.html",
                           tareas=tareas,
                           lote_id=lote_id)


if __name__ == "__main__":

    app.run(debug=True)
