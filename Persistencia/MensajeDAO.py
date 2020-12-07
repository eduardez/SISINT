import Persistencia.DB as DB
from Persistencia.Modelos import Mensaje


def añadirMensaje(fecha_msj,titulo_msj,asunto_msj,cuerpo_msj,grupos_msj):
    mensaje_añadido = Mensaje(fecha=fecha_msj,titulo=titulo_msj,asunto=asunto_msj,cuerpo=cuerpo_msj,grupos=grupos_msj)
    DB.session.add(mensaje_añadido)  
    DB.session.commit() 

def getMensajes():
    consultaMensaje = DB.session.query(Mensaje).order_by(Mensaje.id.desc())
    return consultaMensaje

