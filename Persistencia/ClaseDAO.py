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
    consultaClase = DB.session.query(Clase.id).filter(Clase.clase == int(curso), Clase.letra == str(clase)).all()
    idclase = consultaClase[0]
    DB.session.query(Alumno).filter(Alumno.clase_alumno_id == idclase[0]).delete()
    DB.session.query(Clase).filter(
        Clase.clase == curso,
        Clase.letra == clase
    ).delete()
    DB.session.commit()

def editarClase(curso,clase,cursoN,claseN):
    consultaClase = DB.session.query(Clase).filter(Clase.clase == int(cursoN), Clase.letra == str(claseN)).all()
    if len(consultaClase) == 0:
        DB.session.query(Clase).filter(
            Clase.clase == curso,
            Clase.letra == clase
        ).update({
            Clase.clase: cursoN,
            Clase.letra: claseN
        })
        DB.session.commit()
        return True
    else:
        return False

def getClases():
    consultaClase = DB.session.query(Clase).order_by(Clase.clase.asc(),Clase.letra.asc())
    
    return consultaClase

def buscarClase(codigo):
    curso = codigo[0]
    clase = codigo[1]

    consultaClase = DB.session.query(Clase).filter(Clase.clase == int(curso), Clase.letra == str(clase)).all()
    return consultaClase

