

## NOTA IMPORTANTE: Para poder usar selenium hay que tener en el path el ejecutable "chromedriver"

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time 
import sys
import os
path_dict = {
    'search_box': '//*[@id="side"]/div[1]/div/label/div/div[2]', #Barra de busqueda
    'click_chat_panel': '//*[@id="pane-side"]/div[1]/div[1]/div[1]/div[2]', #Primer panel tras la busqueda
    'chat_input_box': '//*[@id="main"]/footer[1]/div[1]/div[2]/div[1]/div[2]', #Caja input del chat
    'chat_abrir_adjuntar': '//*[@id="main"]/footer[1]/div[1]/div[1]/div[2]/div[1]/div[1]', #Opciones de chat
    'file_input': '//input[@type="file"]', #Path para adjuntar archivo
    'chat_title_name': '/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div/span/text()[1]'
}

# Open WhatsApp URL in chrome browser
RES_PATH = 'Resources'

class WhatsAppController():
    def __init__(self, minimizado=False, browser=None, driver_path=None):
        self.options = None
        self._OS = None
        self.browser = browser
        self.minimizado = minimizado
        self.driver_path = driver_path
        self.driver_folder_tokens = RES_PATH
        self.driver = None
        self.exec = None
        self.wait = None
        #self.driver = webdriver.Chrome(executable_path="/usr/local/share/chromedriver", chrome_options=self.options)
        #self.driver = webdriver.Firefox() ### CON ESTE ME VA A MI EN WINDOWS 10 (SEVILLA)
        self.startController()

    def startController(self):
        if self.driver_path != 'custom':
            self.setBrowser()
            self.setOS()
            self.setBrowserFolder()
        self.setDriverConfig()
        self.startConnection()

    # ------- CONFIGURACIONES Y SELECCION DEL OS -------------
    # ATENCION:
    #     ACTUALMENTE ESTA FUNCION SOLO DA SOPORTE A SO DE 
    #     32b Y 32b&64b, PERO NO DA A SO DE SOLO 64b.
    #     HAY QUE ACTUALIZAR
    # ---------------------------------------------------------
    def setOS(self):
        '''Detectar SO del ordenador'''
        self._OS = sys.platform
        if sys.platform.startswith('linux'):
            self.driver_folder_tokens += '-linux64'
            return 0
        elif self._OS == 'win32':
            self.driver_folder_tokens += '-win32'
            self.exec += '.exe'
            return 0
        elif self._OS == 'darwin':
            self.driver_folder_tokens += '-mac'
            return 0
        else:
            print('OS no detectado. Error.')
            return 1

    def setBrowser(self):
        if self.browser == 'firefox':
            self.driver_folder_tokens += ',geckodriver'
            self.exec = ',geckodriver'
            return 0
        elif self.browser == 'chrome':
            self.driver_folder_tokens += ',chromedriver'
            self.exec = ',chromedriver'
            return 0
        else:
            return 1

    def setBrowserFolder(self):
        self.driver_folder_tokens += self.exec
        split_path = self.driver_folder_tokens.split(",")
        self.driver_path = os.path.join(*split_path)            
        print('\n\n\n \n\nPath encontrado: ' + self.driver_path)

    def setDriverConfig(self):
        if self.browser == 'firefox':
            self.options = webdriver.FirefoxOptions()
            self.driver = webdriver.Firefox(executable_path=self.driver_path)
        elif self.browser == 'chrome':
            self.options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(executable_path=self.driver_path)
            self.options.add_argument(r"user-data-dir=./cache") #Guardar cache

    def toggleSize(self):
        '''Cambiar el tamaño del navegador'''
        if self.minimizado:
            #self.options.add_argument("--headless") #ejecutar minimizado
            #self.options.add_argument("--window-size=0,0") 
            pass
        else:
            #self.options.add_argument("--headless") #ejecutar minimizado
            #self.options.add_argument("--window-size=0,0")
            pass
        self.minimizado = not self.minimizado

    # -------- METODOS DEL WEBDRIVER --------------------------
    def startConnection(self):
        '''Establecer la conexion con la pagina de WP'''
        self.driver.get("https://web.whatsapp.com/")
        print('Estableciendo conexion...')
        self.wait = WebDriverWait(self.driver, 20)
        print('Conexion establecida.')

    def closeDriver(self):
        self.driver.quit()

    # ---------- METODOS DE SELECCION DEL XPATH ----------------
    def searchUser(self, phone):
        '''Buscar telefono en la barra de busqueda'''
        print("Buscando search_box...")
        search_box = self.searchElement('search_box')
        search_box.clear() 
        search_box.send_keys(phone)
        time.sleep(2)
        return True

    def searchAndClick(self, phone):
        '''Buscar telefono en la barra de busqueda y
        hacer click para desplegar el chat'''
        self.searchUser(phone)
        contact_side_pan = self.searchElement('click_chat_panel')
        ActionChains(self.driver).click(contact_side_pan).perform()
        time.sleep(1)
        chat_title = self.searchElement('chat_title_name')
        if not self.cleanString(phone) == self.cleanString(chat_title):
            print("Error encontrando el telefono")
            return 1
        return 0

    def sendMsg(self, text):
        '''Introducir texto en el chat'''
        text_box = self.searchElement('chat_input_box')
        text_box.send_keys(text)

    def adjuntarArchivo(self, path=None):
        abrir_adjuntar_span = self.searchElement('chat_abrir_adjuntar')
        ActionChains(self.driver).click(abrir_adjuntar_span).perform()
        uploader = self.searchElement('file_input')
        uploader.send_keys(path)

    def searchElement(self, element):
        try:
            element = self.wait.until(lambda driver:self.driver.find_element_by_xpath(path_dict[element]))
            print("Encontrado!")
            return element
        except Exception as e:
            print(e)
            print("ERROR: No se ha encontrado el elemento")
            return None

    def cleanString(self, stng):
        return stng



