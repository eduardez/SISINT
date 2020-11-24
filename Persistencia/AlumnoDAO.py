import Persistencia.DB as DB
from Persistencia.Modelos import Alumno, Clase
from sqlalchemy.orm import aliased

def conectarBD(): ### ESTE METODO AL ESTAR EN ALUMNODAO ESTE DA IGUAL, NO SE VA A EJECUTAR NUNCA, HABRÁ QUE QUITARLO.
    #DB.Base.metadata.drop_all(DB.engine) ## Si en algun momento hace falta borrar las filas de toda la base de datos.
    DB.Base.metadata.create_all(DB.engine)

def añadirAlumno(nombre_alu,nombre_tut,tlf,dni,clase_alumno):
    alumno = Alumno(nombre_alumno=nombre_alu,nombre_tutor=nombre_tut,tlf_tutor=tlf,dni_tutor=dni,clase_alumno=clase_alumno)
    DB.session.add(alumno)
    DB.session.commit()

def borrarAlumno(tutor,dni):
    DB.session.query(Alumno).filter(
        Alumno.nombre_tutor == tutor,
        Alumno.dni_tutor == dni
    ).delete()
    DB.session.commit()

def editarAlumno(tutorV,dniV,alumnoN,tutorN,tlfN,dniN,claseN):
    DB.session.query(Alumno).filter(
        Alumno.nombre_tutor == tutorV,
        Alumno.dni_tutor == dniV
    ).update({
        Alumno.nombre_alumno: alumnoN,
        Alumno.nombre_tutor: tutorN,
        Alumno.tlf_tutor: tlfN,
        Alumno.dni_tutor: dniN,
        Alumno.clase_alumno_id: claseN
    })
    DB.session.commit()

def getAlumno():
    consultaAlumno = DB.session.query(Alumno).all()
    
    return consultaAlumno

def getAlumnoPorClase(claseAlumno):
    curso = claseAlumno[0]
    clase = claseAlumno[1]
    consultaAlumno = DB.session.query(Alumno).join(Alumno.clase_alumno).\
        filter(Clase.clase == curso, Clase.letra == clase)\
            .all()
    return consultaAlumno