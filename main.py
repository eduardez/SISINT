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
        self.whatsapp_instance = WhatsAppController(minimizado=False, browser='firefox', driver_installed=False)
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