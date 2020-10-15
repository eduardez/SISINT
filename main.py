#!/usr/bin/env python3

## NOTA IMPORTANTE: Para poder usar selenium hay que tener en el path el ejecutable "chromedriver"

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time


path_dict = {
    'search_box': '//*[@id="side"]/div[1]/div/label/div/div[2]',
    'click_chat_panel': '//*[@id="pane-side"]/div[1]/div[1]/div[1]/div[2]',
    'chat_input_box': '//*[@id="main"]/footer[1]/div[1]/div[2]/div[1]/div[2]'
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

    def sendMsg(self, text, usr):
        if self.searchUser(usr):
            contact_side_pan = self.searchElement('click_chat_panel')
            ActionChains(self.driver).click(contact_side_pan).perform()
            time.sleep(1)
            text_box = self.searchElement('chat_input_box')
            text_box.send_keys(text)

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

if __name__ == "__main__":
    gua = Guasap()
    gua.startConnection()
    user_list = ['34649683729', '34607421849', '34654067118']
    for user in user_list:
        gua.sendMsg("Pruebaca", user)
        time.sleep(0.5)