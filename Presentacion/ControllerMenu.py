import os
import sys

from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QDialogButtonBox, QFormLayout
from PySide2.QtWidgets import QHeaderView, QTableWidgetItem
from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader
from Presentacion.UI_Files.Resources import icons

from Presentacion import ControllerDebug
from Persistencia import ClaseDAO, AlumnoDAO


class Menu:
    def __init__(self, WPController = None):
        super(Menu, self).__init__()
        self.ui = QUiLoader().load(QFile("Presentacion/UI_Files/UI_menu.ui"))
        ### PARA WINDOWS (SEVILLA)
        #self.ui = QUiLoader().load(QFile("C:\\Users\\sevil\\Desktop\\SISINT-persistencia\\Presentacion\\UI_Files\\UI_menu.ui"))
        self.wp_controller = WPController
        self.iniciarDB()
        self.setActions()
        self.setClases()
        self.setTablaClase()
        self.adjustTables()
        self.ui.stackedWidget.setCurrentIndex(3)

    def _exec(self):
        self.ui.show()

    def iniciarDB(self): 
        ClaseDAO.conectarBD()

    def setActions(self):
        self.ui.btn_enviar.clicked.connect(self.enviarmsg)
        self.ui.btn_mensajes.clicked.connect(self.mensajes)
        self.ui.btn_colegios.clicked.connect(self.colegio)
        self.ui.btn_settings.clicked.connect(self.openDebugSettings)

    def adjustTables(self):
        tablas = [self.ui.tableWidget, self.ui.tbl_alumnos, self.ui.tbl_clases]
        for tbl in tablas:
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tbl.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def enviarmsg(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.btn_forms.clicked.connect(self.crear_googleforms)

    def crear_googleforms(self):
        webbrowser.open('https://www.google.com/intl/es_es/forms/about/') # no se que es webbrowser y por eso no va el boton

    def mensajes(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.btn_masivo.clicked.connect(self.ver_googleforms)

    def ver_googleforms(self):
        webbrowser.open('https://www.google.com/intl/es_es/forms/about/') # no se que es webbrowser y por eso no va el boton

    def colegio(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        ####### BOTONES PESTAÑA ALUMNO #######
        self.ui.btn_addalu.clicked.connect(self.añadirAlumno)
        self.ui.btn_editalu.clicked.connect(self.editarAlumno)
        self.ui.btn_borraralu.clicked.connect(self.borrarAlumno)
        ####### BOTONES PESTAÑA CLASES #######
        self.ui.btn_addclase.clicked.connect(self.añadirClase)
        self.ui.btn_editclase.clicked.connect(self.editarClase)
        self.ui.btn_borrarclase.clicked.connect(self.borrarClase)
        
    def openDebugSettings(self):
        deb = ControllerDebug.DebugFrame(self.wp_controller)
        deb.ui.exec_()

################ FUNCIONES COLEGIO PESTAÑA ALUMNO #######################
    def añadirAlumno(self):
        alumno = InputDialog_Alumno()
        alumno.exec()
        nombre_alu, nombre_tut, tlf, dni = alumno.getInputs()
        AlumnoDAO.añadirAlumno(nombre_alu,nombre_tut,tlf,dni)
    def editarAlumno(self):
        pass

    def borrarAlumno(self):
        pass
################ FUNCIONES COLEGIO PESTAÑA CLASES #######################
 
    def añadirClase(self):
        clase = InputDialog_Clase()
        clase.exec()
        curso, letra = clase.getInputs()
        ClaseDAO.añadirClase(curso,letra)
        self.setClases()
        self.setTablaClase() ### Para que se muestre la nueva fila añadida en la tabla.

    def editarClase(self):
        row = self.ui.tbl_clases.currentRow()
        cursoV = self.ui.tbl_clases.item(row, 0)
        letraV = self.ui.tbl_clases.item(row, 1)
        if (cursoV.text() == None) : ### Este IF ELSE NO FUNCIONA MUY BIEN
            print("NO HAY TEXTO, NO SE PUEDE EDITAR")
        else:
            clase = InputDialog_Clase()
            clase.exec()
            cursoN, letraN = clase.getInputs()
            ClaseDAO.editarClase(cursoV.text(),letraV.text(),cursoN,letraN)
            self.setClases()
            self.setTablaClase() # Para que se muestre la nueva fila editada en la tabla.

    def borrarClase(self):
        row = self.ui.tbl_clases.currentRow()
        curso = self.ui.tbl_clases.item(row, 0)
        letra = self.ui.tbl_clases.item(row, 1)
        ClaseDAO.borrarClase(curso.text(),letra.text()) # Se borra de la bbdd.
        self.setClases()
        self.setTablaClase() # Para que se muestre la nueva tabla, con el registro borrado.

    def setClases(self):
        self.ui.cb_selgrupo.clear()
        items = ClaseDAO.getClases()
        items_añadir = []
        for i in items:
            items_añadir.append(i.__str__())
        self.ui.cb_selgrupo.addItems(items_añadir)
    
    def setTablaClase(self):
        self.ui.tbl_clases.clearContents() #### Borrar la tabla y volver a recorrer los registros de la BBDD (PIERDE LA CABECERA)
        items = ClaseDAO.getClases()
        contador = 0
        for i in items:
            numRows = self.ui.tbl_clases.rowCount()
            self.ui.tbl_clases.insertRow(contador)
            
            curso = i.getClase()
            clase = i.getLetra()

            item = QTableWidgetItem(str(curso))
            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.ui.tbl_clases.setItem(contador,0,item)

            item = QTableWidgetItem(clase)
            item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            self.ui.tbl_clases.setItem(contador,1,item)

            contador = contador + 1

class InputDialog_Clase(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Datos Clase")
        self.first = QLineEdit(self)
        self.second = QLineEdit(self)

        self.onlyInt = QtGui.QIntValidator()
        self.first.setValidator(self.onlyInt)

        reg_ex = QtCore.QRegExp("[A-Z]")
        input_validator = QtGui.QRegExpValidator(reg_ex,self)
        self.second.setValidator(input_validator)

        self.first.setMaxLength(1)
        self.second.setMaxLength(1)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("Curso", self.first)
        layout.addRow("Clase", self.second)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.second.text())

class InputDialog_Alumno(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Datos Alumno")
        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        self.third = QLineEdit(self)
        self.fourth = QLineEdit(self)

        reg_ex = QtCore.QRegExp("[A-Za-z]+")
        input_validator = QtGui.QRegExpValidator(reg_ex,self)
        self.first.setValidator(input_validator)
        self.second.setValidator(input_validator)

        self.onlyInt = QtGui.QIntValidator()
        self.third.setValidator(self.onlyInt)

        self.first.setMaxLength(30)
        self.second.setMaxLength(30)
        self.third.setMaxLength(9)
        self.fourth.setMaxLength(9)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("Alumno", self.first)
        layout.addRow("Tutor", self.second)
        layout.addRow("Tlf.", self.third)
        layout.addRow("DNI", self.fourth)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.second.text(), self.third.text(), self.fourth.text())      
        
