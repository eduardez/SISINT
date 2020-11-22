import Persistencia.DB as DB
from Persistencia.Modelos import Alumno, Clase

def conectarBD(self):
    DB.Base.metadata.create_all(DB.engine)

def añadirClase(curso,clase):
    clase = Clase(clase=curso,letra=clase)
    DB.session.add(clase)
    DB.session.commit()

def getClases():
    consultaClase = DB.session.query(Clase).all()
    
    return consultaClase

