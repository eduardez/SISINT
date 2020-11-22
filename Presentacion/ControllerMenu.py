import os
import sys

from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QDialogButtonBox, QFormLayout
from PySide2.QtWidgets import QHeaderView, QTableWidgetItem
from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader
from Presentacion.UI_Files.Resources import icons

from Presentacion import ControllerDebug
from Persistencia import ClaseDAO


class Menu:
    def __init__(self, WPController = None):
        super(Menu, self).__init__()
        self.ui = QUiLoader().load(QFile("Presentacion/UI_Files/UI_menu.ui"))
        self.wp_controller = WPController
        self.setActions()
        self.setClases()
        self.setTablaClase()
        self.adjustTables()
        self.ui.stackedWidget.setCurrentIndex(3)

    def _exec(self):
        self.ui.show()

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
        webbrowser.open('https://www.google.com/intl/es_es/forms/about/')

    def mensajes(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.btn_masivo.clicked.connect(self.ver_googleforms)

    def ver_googleforms(self):
        webbrowser.open('https://www.google.com/intl/es_es/forms/about/')

    def colegio(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        #nuevo
        self.ui.btn_addclase.clicked.connect(self.mostrarInput)
        

    def openDebugSettings(self):
        deb = ControllerDebug.DebugFrame(self.wp_controller)
        deb.ui.exec_()
    
    """     Nuevo    """

    def mostrarInput(self):
        clase = InputDialog()
        clase.exec()
        curso, letra = clase.getInputs()
        print(curso)
        print(letra)
        ClaseDAO.añadirClase(curso,letra)
        self.setClases()


    def setClases(self):
        self.ui.cb_selgrupo.clear()
        items = ClaseDAO.getClases()
        items_añadir = []
        for i in items:
            items_añadir.append(i.__str__())
        self.ui.cb_selgrupo.addItems(items_añadir)
    
    def setTablaClase(self):
        items = ClaseDAO.getClases()
        
        #self.ui.tbl_clases.insertRow(len(items))
        #print(len(items))
        #self.ui.tbl_clases.setItem(0,0,QTableWidgetItem("curso"))
        #self.ui.tbl_clases.setItem(0,1,QTableWidgetItem("clase"))
        contador1 = 0
        contador2 = 0
        for i in items:
            numRows = self.ui.tbl_clases.rowCount()
            self.ui.tbl_clases.insertRow(numRows)
            curso = i.getClase()
            clase = i.getLetra()

            item = QTableWidgetItem(str(curso))

            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            
            self.ui.tbl_clases.setItem(numRows,0,item)

            item = QTableWidgetItem(clase)

            item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            self.ui.tbl_clases.setItem(numRows,1,item)
            #contador1+=1
        #self.ui.tbl_clases.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

#modificar
class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        

        self.first = QLineEdit(self)
        self.second = QLineEdit(self)

        self.onlyInt = QtGui.QIntValidator()
        #self.onlyMayus = QtGui.Q
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
        
    
        
