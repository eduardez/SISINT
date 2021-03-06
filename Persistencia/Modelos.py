import Persistencia.DB as DB

from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship, backref


class Alumno(DB.Base):
    __tablename__ = 'alumnos'

    nombre_alumno = Column(String(30), primary_key = True)
    nombre_tutor = Column(String(30), nullable = False)
    tlf_tutor = Column(String(9), nullable = False, unique = True)
    dni_tutor = Column(String(9), nullable = False, unique = True)
    clase_alumno_id = Column(Integer, ForeignKey('clases.id',ondelete='CASCADE'))
    clase_alumno = relationship('Clase',cascade='delete',backref=backref('clases',passive_deletes=True))

    def getNombreAlumno(self):
        return self.nombre_alumno

    def getNombreTutor(self):
        return self.nombre_tutor
    
    def getTelefono(self):
        return self.tlf_tutor

    def getDNI(self):
        return self.dni_tutor
    
    def __str__(self):
        return self.nombre_alumno + " clase: "+ str(self.clase_alumno)

class Clase(DB.Base):
    __tablename__ = 'clases'

    id = Column(Integer(), primary_key = True)
    clase = Column(Integer())
    letra = Column(String(1))

    def getClase(self):
        return self.clase
    
    def getLetra(self):
        return self.letra

    def __str__(self):
        return str(self.clase)+self.letra