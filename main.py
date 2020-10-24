#!/usr/bin/env python3

import time
import cmd

class MainMenu(cmd.Cmd):
    #guasap = Guasap()
    intro = 'Watsss 0.0.1'
    prompt = 'WPConsole > '
    
    def do_connect(self, args):
        self.guasap.startConnection()
        
    def do_disconnect(self, args):
        self.guasap.closeDriver()
    
    def do_sendMsgUser(self, args):
        msg = input('Mensaje: ')
        user = input('Usuario: ')
        if self.guasap.searchUser(user):
            self.guasap.sendMsg(msg)
        else:
            #Aqui ver si el titulo del chat activo se corresponde con el del usuario
            print('Usuario no encontrado')

    def do_adjuntar(self, args):
        self.guasap.adjuntarArchivo()

    def do_searchUser(self, args):
        user = input('Usuario: ')
        self.guasap.searchUser(user)

    def do_sendMsg(self, args):
        msg = input('Mensaje: ')
        self.guasap.sendMsg(msg)
    
    def do_getInfo(self, args):
        logger.other('Device {0}'.format(self.device_clock.mac_addr))
    
    def do_vibrate(self, args):
        self.device_clock.vibrate()

    def do_exit(self, arg):
        logger.success('Bye coneho')
        return True


from Presentacion import UI_Principal_CONT
from Dominio.WhatsappController import Guasap


if __name__ == "__main__":
    #MainMenu().cmdloop()
    whatsapp_instance = Guasap()
    UI_Principal_CONT.start(whatsapp_instance)
