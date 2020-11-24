#!/usr/bin/env python3

import time
import cmd
import logging
from PyQt5.QtWidgets import QApplication, QDialog
import sys
from PyQt5 import QtGui

from Dominio.WhatsappController import WhatsAppController
from Presentacion import ControllerLogin, ControllerMenu

class NombreApp:
    def __init__(self):
        self.logger = logging.getLogger('main')
        self.whatsapp_instance = None
        self.login_controller_instance = None
        self.menu_controller_instance = None
        # -------------
        self.isLogged = False
        # -------------
        self.initInstances()
        self.initFiles()
        self.startApp()

    def initInstances(self):
        '''Inicializacion de controladores, bbdd y otros'''
        self.whatsapp_instance = WhatsAppController()
        self.login_controller_instance = ControllerLogin.Login()
        self.menu_controller_instance = ControllerMenu.Menu(self.whatsapp_instance)
        self.logger.info('Inicializacion de instancias completada')

    def initFiles(self):
        '''Comprobacion de archivos en el sistema (selenium, 
        chromedriver, drivers bbdd, ...)'''

        self.logger.info('Inicializacion de recursos completada')

    def cleanInstances(self):
        '''Limpiar instancias persistentes y drivers'''
        self.whatsapp_instance.closeDriver()
        sys.exit(1)

    def startApp(self):
        '''Comenzar el flujo principal de la aplicacion'''
        self.logger.info('Iniciando App...')
        if(self.login_controller_instance.ui.exec_() == QDialog.Accepted):
            self.menu_controller_instance._exec()
        else:
            self.cleanInstances()   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    new_instance = NombreApp()
    app.aboutToQuit.connect(lambda: new_instance.cleanInstances())
    sys.exit(app.exec_())


# class MainMenu(cmd.Cmd):
#     #guasap = Guasap()
#     intro = 'Watsss 0.0.1'
#     prompt = 'WPConsole > '
    
#     def do_connect(self, args):
#         self.guasap.startConnection()
        
#     def do_disconnect(self, args):
#         self.guasap.closeDriver()
    
#     def do_sendMsgUser(self, args):
#         msg = input('Mensaje: ')
#         user = input('Usuario: ')
#         if self.guasap.searchUser(user):
#             self.guasap.sendMsg(msg)
#         else:
#             #Aqui ver si el titulo del chat activo se corresponde con el del usuario
#             print('Usuario no encontrado')

#     def do_adjuntar(self, args):
#         self.guasap.adjuntarArchivo()

#     def do_searchUser(self, args):
#         user = input('Usuario: ')
#         self.guasap.searchUser(user)

#     def do_sendMsg(self, args):
#         msg = input('Mensaje: ')
#         self.guasap.sendMsg(msg)
    
#     def do_getInfo(self, args):
#         logger.other('Device {0}'.format(self.device_clock.mac_addr))
    
#     def do_vibrate(self, args):
#         self.device_clock.vibrate()

#     def do_exit(self, arg):
#         logger.success('Bye coneho')
#         return True
