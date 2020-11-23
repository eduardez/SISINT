import Persistencia.DB as DB
from Persistencia.Modelos import Alumno, Clase

def conectarBD():
    #DB.Base.metadata.drop_all(DB.engine) ## Si en algun momento hace falta borrar las filas de toda la base de datos.
    DB.Base.metadata.create_all(DB.engine)

def eliminarBD():
    DB.Base.metadata.drop_all(DB.engine)


def añadirClase(curso,clase):
    clase_añadida = Clase(clase=curso,letra=clase)
    consultaClase = DB.session.query(Clase).filter(Clase.clase == int(curso), Clase.letra == str(clase)).all()
    if len(consultaClase) == 0:
        DB.session.add(clase_añadida)   
        DB.session.commit()
        return True
    else:
        return False

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
    consultaClase = DB.session.query(Clase).order_by(Clase.clase.asc(),Clase.letra.asc())
    
    return consultaClase

def buscarClase(codigo):
    curso = codigo[0]
    clase = codigo[1]

    consultaClase = DB.session.query(Clase).filter(Clase.clase == int(curso), Clase.letra == str(clase)).all()
    return consultaClase



