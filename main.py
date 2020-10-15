#!/usr/bin/env python3

## NOTA IMPORTANTE: Para poder usar selenium hay que tener en el path el ejecutable "chromedriver"

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import cmd

path_dict = {
    'search_box': '//*[@id="side"]/div[1]/div/label/div/div[2]',
    'click_chat_panel': '//*[@id="pane-side"]/div[1]/div[1]/div[1]/div[2]',
    'chat_input_box': '//*[@id="main"]/footer[1]/div[1]/div[2]/div[1]/div[2]',
    'chat_abrir_adjuntar': '//*[@id="main"]/footer[1]/div[1]/div[1]/div[2]/div[1]/div[1]',
    'file_input': '//input[@type="file"]'
}

# Open WhatsApp URL in chrome browser


class Guasap():
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir=./cache") #Guardar cache
        self.wait = None
        self.driver = webdriver.Chrome(executable_path="/usr/local/share/chromedriver", chrome_options=self.options)
        

    def startConnection(self):
        self.driver.get("https://web.whatsapp.com/")
        print('Estableciendo conexion...')
        self.wait = WebDriverWait(self.driver, 20)
        print('Conexion establecida.')

    def searchUser(self, usr):
        print("Buscando search_box...")
        person_title = self.searchElement('search_box')
        person_title.clear()
        person_title.send_keys(usr)
        time.sleep(2)
        return True

    def sendMsg(self, text):
        contact_side_pan = self.searchElement('click_chat_panel')
        ActionChains(self.driver).click(contact_side_pan).perform()
        time.sleep(1)
        text_box = self.searchElement('chat_input_box')
        text_box.send_keys(text)

    def adjuntarArchivo(self):
        abrir_adjuntar_span = self.searchElement('chat_abrir_adjuntar')
        ActionChains(self.driver).click(abrir_adjuntar_span).perform()
        uploader = self.searchElement('file_input')
        uploader.send_keys('/home/eduardez/Escritorio/Workspace/LAB_INTERRACT/SISINT/README.md')


    def searchElement(self, element):
        try:
            element = self.wait.until(lambda driver:self.driver.find_element_by_xpath(path_dict[element]))
            print("Encontrado!")
            return element
        except Exception as e:
            print(e)
            print("ERROR: No se ha encontrado el elemento")
            return None

    def closeDriver(self):
        self.driver.quit()


class MainMenu(cmd.Cmd):
    guasap = Guasap()
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




if __name__ == "__main__":
    MainMenu().cmdloop()