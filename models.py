from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Propiedades(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    id_propiedad  = db.Column(db.Integer)
    nombre = db.Column(db.String(80), unique=True)
    precio = db.Column(db.Integer, unique=True)
    minMet = db.Column(db.Float)
    maxMet = db.Column(db.Float)
    precio_m2 = db.Column(db.Float)
    direc  = db.Column(db.Text)
    tipo   = db.Column(db.Text)
    lat    = db.Column(db.Float)
    lon = db.Column(db.Float)
    dorms = db.Column(db.Integer)
    banios = db.Column(db.Integer)
    fechaPub = db.Column(db.DateTime)
    fechaScrap = db.Column(db.DateTime)
    link = db.Column(db.Text)



def save(masters):
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
            propiedad.tipo = master[8]
            propiedad.lat = master[9]
            propiedad.lon = master[10]
            propiedad.dorms = master[11]
            propiedad.banios = master[12]
            propiedad.fechaPub = master[13]
            propiedad.link = master[14]

            propiedad.fechaScrap = time.time()

            db.session.add(propiedad)
        else:
            propiedad.nombre = master[1]
            propiedad.precio = master[2]
            propiedad.minMet = master[4]
            propiedad.maxMet = master[5]
            propiedad.precio_m2 = master[6]
            propiedad.direc = master[7]
            propiedad.tipo = master[8]
            propiedad.lat = master[9]
            propiedad.lon = master[10]
            propiedad.dorms = master[11]
            propiedad.banios = master[12]
            propiedad.fechaPub = master[13]
            propiedad.link = master[14]

            propiedad.fechaScrap = time.time()

    db.session.commit()

if __name__ == "__main__":
    db.create_all()