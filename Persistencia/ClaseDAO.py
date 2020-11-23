import Persistencia.DB as DB
from Persistencia.Modelos import Alumno, Clase

def conectarBD():
    #DB.Base.metadata.drop_all(DB.engine) ## Si en algun momento hace falta borrar las filas de toda la base de datos.
    DB.Base.metadata.create_all(DB.engine)

def añadirClase(curso,clase):
    clase = Clase(clase=curso,letra=clase)
    DB.session.add(clase)
    DB.session.commit()

def borrarClase(curso,clase):
    DB.session.query(Clase).filter(
        Clase.clase == curso,
        Clase.letra == clase
    ).delete()
    DB.session.commit()

def editarClase(curso,clase,cursoN,claseN):
    DB.session.query(Clase).filter(
        Clase.clase == curso,
        Clase.letra == clase
    ).update({
        Clase.clase: cursoN,
        Clase.letra: claseN
    })
    DB.session.commit()

def getClases():
    consultaClase = DB.session.query(Clase).all()
    
    return consultaClase

