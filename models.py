from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Propiedades(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    id_propiedad  = db.Column(db.Integer, unique=True)
    comuna = db.Column(db.String(80))
    operacion = db.Column(db.String(80))
    nombre = db.Column(db.String(80))
    precio = db.Column(db.Integer)
    minMet = db.Column(db.Float)
    maxMet = db.Column(db.Float)
    precio_m2 = db.Column(db.Float)
    direc  = db.Column(db.Text)
    clase   = db.Column(db.Text)
    lat    = db.Column(db.Float)
    lon = db.Column(db.Float)
    dorms = db.Column(db.Integer)
    banios = db.Column(db.Integer)
    fechaPub = db.Column(db.DateTime)
    fechaScrap = db.Column(db.DateTime)
    link = db.Column(db.Text)
    tipo = db.Column(db.Text)

def read():
    props = Propiedades().query.all()
    return props

def readVentaDpto():
    props = Propiedades.query.filter_by(tipo='departamento',operacion='venta').all()
    return props

def save(masters):
    print("Saving onto db...")
    for master in masters:
        propiedad = Propiedades().query.filter_by(id_propiedad=master[0]).first()
        if propiedad == None:
            propiedad = Propiedades()
            propiedad.id_propiedad = master[0]
            propiedad.nombre = master[1]
            propiedad.precio = master[2]
            propiedad.minMet = master[4]
            propiedad.maxMet = master[5]
            propiedad.precio_m2 = master[6]
            propiedad.direc = master[7]
            propiedad.clase = master[8]
            propiedad.lat = master[9]
            propiedad.lon = master[10]
            propiedad.dorms = master[11]
            propiedad.banios = master[12]

            dateStr = master[13]
            if dateStr != "-":
                date = datetime.date(day=int(dateStr[:2]),year= int(dateStr[6:]), month=int(dateStr[3:5]))
            else:
                date = datetime.date(day=1,month=1,year=1000)
            propiedad.fechaPub = date
            propiedad.link = master[14]

            propiedad.fechaScrap = datetime.datetime.now()

            propiedad.operacion=master[15]
            propiedad.comuna=master[16]
            propiedad.tipo = master[17]

            db.session.add(propiedad)
        else:
            propiedad.nombre = master[1]
            propiedad.precio = master[2]
            propiedad.minMet = master[4]
            propiedad.maxMet = master[5]
            propiedad.precio_m2 = master[6]
            propiedad.direc = master[7]
            propiedad.clase = master[8]
            propiedad.lat = master[9]
            propiedad.lon = master[10]
            propiedad.dorms = master[11]
            propiedad.banios = master[12]

            dateStr = master[13]
            if dateStr != "-":
                date = datetime.date(day=int(dateStr[:2]), year=int(dateStr[6:]), month=int(dateStr[3:5]))
            else:
                date = datetime.date(day=1, month=1, year=1000)
            propiedad.fechaPub = date

            propiedad.fechaScrap = datetime.datetime.now()

            propiedad.link = master[14]

            propiedad.operacion=master[15]
            propiedad.comuna=master[16]
            propiedad.tipo = master[17]


    db.session.commit()

if __name__ == "__main__":
    db.create_all()