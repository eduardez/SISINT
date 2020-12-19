import os
import sys
import webbrowser
import datetime ##### Fecha de hoy ----> today = datetime.date.today()

from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QDialogButtonBox, QFormLayout, QComboBox, QFileDialog
from PySide2.QtWidgets import QHeaderView, QTableWidgetItem, QMessageBox, QFrame, QTreeWidgetItem, QCheckBox, QFileDialog
from PySide2.QtCore import QFile, Qt, QDir
from PySide2.QtUiTools import QUiLoader
from Presentacion.UI_Files.Resources import icons

from Presentacion import ControllerDebug,ControllerLogin
from Persistencia import ClaseDAO, AlumnoDAO, MensajeDAO


class Menu:
    GRUPOS = []
    GRUPOS_SELECCIONADOS = []
    def __init__(self, WPController = None):
        super(Menu, self).__init__()
        self.ui = QUiLoader().load(QFile("Presentacion/UI_Files/UI_menu.ui"))
        ### PARA WINDOWS (SEVILLA)
        #self.ui = QUiLoader().load(QFile("C:\\Users\\sevil\\Desktop\\SISINT-Controlador\\Presentacion\\UI_Files\\UI_menu.ui"))
        self.wp_controller = WPController
        self.iniciarDB()
        self.setActions()
        self.setClases()
        self.setTablaClase()
        self.adjustTables()
        self.ui.stackedWidget.setCurrentIndex(3)
        # Método para conectar base de datos
        ClaseDAO.conectarBD()
        # Método para eliminar toda la base de datos
        #ClaseDAO.eliminarBD()
        self.setTablaAlumno()
        self.setTreeGrupos()
        self.setActionsMSG()
        self.setActionsMensajes()
        self.setActionsColegio()

    def _exec(self):
        self.ui.show()

    def iniciarDB(self): 
        ClaseDAO.conectarBD()

    def setActions(self):
        self.ui.btn_user.clicked.connect(self.inicio)
        self.ui.btn_enviar.clicked.connect(self.enviarmsg)
        self.ui.btn_mensajes.clicked.connect(self.mensajes)
        self.ui.btn_colegios.clicked.connect(self.colegio)
        self.ui.btn_settings.clicked.connect(self.openDebugSettings)
        self.ui.btn_salir.clicked.connect(self.salirApp)

    def setActionsMSG(self):
        self.ui.btn_forms.clicked.connect(self.crear_googleforms)
        self.setGruposEnviarMensajes()
        self.ui.btn_masivo.clicked.connect(self.enviarMensaje)
        self.ui.treeGrupos.itemChanged.connect(self.cambioTree)
    
    def setActionsMensajes(self):
        self.cargarMensajesHistorial()
        self.ui.pushButton.clicked.connect(self.ver_googleforms)
    
    def setActionsColegio(self):
        ####### BOTONES PESTAÑA ALUMNO #######
        self.ui.btn_addalu.clicked.connect(self.añadirAlumno)
        self.ui.btn_editalu.clicked.connect(self.editarAlumno)
        self.ui.btn_borraralu.clicked.connect(self.borrarAlumno)
        self.ui.cb_selgrupo.currentTextChanged.connect(self.setTablaAlumno)
        ####### BOTONES PESTAÑA CLASES #######
        self.ui.btn_addclase.clicked.connect(self.añadirClase)
        self.ui.btn_editclase.clicked.connect(self.editarClase)
        self.ui.btn_borrarclase.clicked.connect(self.borrarClase)
        

    def adjustTables(self):
        tablas = [self.ui.tbl_historial, self.ui.tbl_alumnos, self.ui.tbl_clases]
        for tbl in tablas:
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tbl.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def inicio(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def enviarmsg(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        

    def crear_googleforms(self):
        webbrowser.open('https://www.google.com/intl/es_es/forms/about/') 

    def mensajes(self):
        self.cargarMensajesHistorial()
        self.ui.stackedWidget.setCurrentIndex(1)

    def ver_googleforms(self):
        webbrowser.open('https://www.google.com/intl/es_es/forms/about/')

    def colegio(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        
    def salirApp(self):
        self.ui.close()

    def openDebugSettings(self):
        deb = ControllerDebug.DebugFrame(self.wp_controller)
        deb.ui.exec_()

################ FUNCIONES ENVIAR MENSAJE ###############################

    def setGrupos(self):
        self.GRUPOS = []
        numGrupos = self.ui.treeGrupos.topLevelItemCount()
        for i in range(0,numGrupos):
            self.GRUPOS.append(self.ui.treeGrupos.topLevelItem(i))
        print(self.GRUPOS)

    def setTreeGrupos(self):
        self.ui.treeGrupos.blockSignals(True)
        self.ui.treeGrupos.clear()
        items = ClaseDAO.getClases()
        clases = []
        for i in items:
            clases.append(i.__str__())
        grupos = {}

        grupo = clases[0][0]
        clases_grupo = []
        for i in clases:
            if i[0] != grupo and grupo != "":
                grupos[grupo] = clases_grupo
            #if i[0] not in grupos:
                clases_grupo = []
                grupo = i[0]
                clases_grupo.append(i)
            else:
                clases_grupo.append(i)
        grupos[grupo] = clases_grupo
        
        for grupo,clases in grupos.items():
            parent = QTreeWidgetItem(self.ui.treeGrupos)
            parent.setText(0,grupo)
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            
            for x in clases:
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0,"{0}".format(x))
                child.setCheckState(0,Qt.Unchecked)
        self.ui.treeGrupos.blockSignals(False)
        self.setGrupos()

    def setGruposEnviarMensajes(self):
        items = ClaseDAO.getClases()
        clases = []
        for i in items:
            clases.append(i.__str__())
    
    def cambioTree(self,item,column):
        if item.checkState(column) == QtCore.Qt.Checked:
            print('{}: Item Checked'.format(item.text(0)))
            if item not in self.GRUPOS:
                if item.parent() not in self.GRUPOS_SELECCIONADOS:
                    #self.GRUPOS_SELECCIONADOS.append(item.parent()) # No hay que meter el padre, si no los hijos.
                    self.GRUPOS_SELECCIONADOS.append(item)
                    self.ui.txt_n_grupos.setText(str(len(self.GRUPOS_SELECCIONADOS)))
                numero = int(self.ui.txt_n_clases.text())
                numero += 1
                self.ui.txt_n_clases.setText(str(numero))
                num_alumnos = int(self.ui.txt_n_alumnos.text())
                curso = item.text(0)[0]
                clase = item.text(0)[1]
                num_alumnos += len(AlumnoDAO.getAlumnoPorClase(str(curso)+clase))
                self.ui.txt_n_alumnos.setText(str(num_alumnos))

        elif item.checkState(column) == QtCore.Qt.Unchecked:
            print('{}: Item Unchecked'.format(item.text(0)))
            if item not in self.GRUPOS:
                numero = int(self.ui.txt_n_clases.text())
                numero -= 1
                self.ui.txt_n_clases.setText(str(numero))
                num_alumnos = int(self.ui.txt_n_alumnos.text())
                curso = item.text(0)[0]
                clase = item.text(0)[1]
                num_alumnos -= len(AlumnoDAO.getAlumnoPorClase(str(curso)+clase))
                self.ui.txt_n_alumnos.setText(str(num_alumnos))
            else:
                self.GRUPOS_SELECCIONADOS.remove(item) #### SI QUITAS UN CHECK PETA AQUÍ, I DONT KNOW.
                self.ui.txt_n_grupos.setText(str(len(self.GRUPOS_SELECCIONADOS)))

    def enviarMensaje(self):
        ####### Meter el mensaje en la tabla del historial de mensajes #######
        today = datetime.date.today()
        fecha = today.strftime("%b %d %Y")
        titulo = self.ui.le_titulo.text()
        asunto = self.ui.le_asunto.text()
        cuerpo = self.ui.le_cuerpo.toPlainText()
        grupos = ""

        for i in range(0,len(self.GRUPOS_SELECCIONADOS)):
            print(self.GRUPOS_SELECCIONADOS[i].text(0))
            grupos = grupos + self.GRUPOS_SELECCIONADOS[i].text(0) + " "

        if titulo == "" or asunto == "" or cuerpo == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("Algún campo está vacío.")
            msg.setWindowTitle("Error")
            msg.exec_()
        else: 
            #### OBTENCIÓN DE TELÉFONOS PARA REALIZAR EL ENVÍO MÁSIVO.
            telefonos = []
            for i in range(0,len(self.GRUPOS_SELECCIONADOS)):
                items = AlumnoDAO.getAlumnoPorClase(self.GRUPOS_SELECCIONADOS[i].text(0))
                for i in items:
                    telefonos.append(i.getTelefono())   
            print(telefonos)

            #### AÑADIR EL MENSAJE AL HISTORIAL DE MENSAJES.
            MensajeDAO.añadirMensaje(fecha,titulo,asunto,cuerpo,grupos) 
            #### ENVÍO MASIVO
            self.wp_controller.sentMultiMsg(telefonos, cuerpo, True, titulo, asunto) # a False no envía, a true sí.

            #### VACIADO DE CAMPOS.
            self.ui.le_titulo.clear()
            self.ui.le_asunto.clear()
            self.ui.le_cuerpo.clear()

################ FUNCIONES PESTAÑA HISTORIAL #######################
    def cargarMensajesHistorial(self):
        self.borrarTabla(self.ui.tbl_historial)
        items = MensajeDAO.getMensajes()
        contador = 0
        for i in items:
            self.ui.tbl_historial.insertRow(contador)
            fecha = i.getFecha()
            titulo = i.getTitulo()
            asunto = i.getAsunto()
            cuerpo = i.getCuerpo()
            grupos = i.getGrupos()

            item = QTableWidgetItem(fecha)
            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.ui.tbl_historial.setItem(contador,0,item)

            item = QTableWidgetItem(titulo)
            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.ui.tbl_historial.setItem(contador,1,item)

            item = QTableWidgetItem(asunto)
            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.ui.tbl_historial.setItem(contador,2,item)

            item = QTableWidgetItem(cuerpo)
            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.ui.tbl_historial.setItem(contador,3,item)

            item = QTableWidgetItem(grupos)
            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.ui.tbl_historial.setItem(contador,4,item)

            contador = contador + 1

################ FUNCIONES COLEGIO PESTAÑA ALUMNO #######################
    
    def añadirAlumno(self):
        aux = []
        items = ClaseDAO.getClases()
        clases = []
        for i in items:
            clases.append(i.__str__())

        alumno = InputDialog_Alumno(aux,clases)
        añadir = alumno.exec()
        if añadir == 1:
            nombre_alu, nombre_tut, tlf, dni, clase = alumno.getInputs()
            clase_alumno = ClaseDAO.buscarClase(clase)
            for i in clase_alumno:
                c_alumno = i
            valor = AlumnoDAO.añadirAlumno(nombre_alu,nombre_tut,tlf,dni,c_alumno)
            if valor == True:
                self.setTablaAlumno()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText("El DNI o el teléfono ya estaba anteriormente introducido.")
                msg.setWindowTitle("Error")
                msg.exec_()
            

    def editarAlumno(self): 
        row = self.ui.tbl_alumnos.currentRow()
        nombre_v = self.ui.tbl_alumnos.item(row, 0)
        tutor_v = self.ui.tbl_alumnos.item(row, 1)
        tlf_v = self.ui.tbl_alumnos.item(row, 2)
        dni_v = self.ui.tbl_alumnos.item(row, 3)
        if (tutor_v == None): ### Si no selecciona ninguna fila
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("Debes seleccionar el alumno a editar.")
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            alumno_elegido = [nombre_v.text(),tutor_v.text(),tlf_v.text(),dni_v.text()]
            items = ClaseDAO.getClases()
            clases = []
            for i in items:
                clases.append(i.__str__())

            alumno = InputDialog_Alumno(alumno_elegido,clases)
            editar = alumno.exec()
            if editar == 1:
                nombre_alu, nombre_tut, tlf, dni, clase = alumno.getInputs()
                clase_alumno = ClaseDAO.buscarClase(clase)
                for i in clase_alumno:
                    c_alumno = i
                AlumnoDAO.editarAlumno(tutor_v.text(),dni_v.text(),nombre_alu,nombre_tut,tlf,dni,c_alumno)
                self.setTablaAlumno()

    def borrarAlumno(self):
        row = self.ui.tbl_alumnos.currentRow()
        tutor = self.ui.tbl_alumnos.item(row, 1)
        dni = self.ui.tbl_alumnos.item(row, 3)
        if (tutor == None):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("Debes seleccionar el alumno a eliminar.")
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            AlumnoDAO.borrarAlumno(tutor.text(),dni.text()) # Se borra de la bbdd.
            self.setClases()
            self.setTablaAlumno() # Para que se muestre la nueva tabla, con el registro borrado.

    def setTablaAlumno(self):
        clase_actual = self.ui.cb_selgrupo.currentText()
        if clase_actual != "":
            alumnos = AlumnoDAO.getAlumnoPorClase(clase_actual)
            
            self.borrarTabla(self.ui.tbl_alumnos)
            contador = 0
            for a in alumnos:
                numRows = self.ui.tbl_alumnos.rowCount()
                self.ui.tbl_alumnos.insertRow(contador)
                
                nombre_alumno = a.getNombreAlumno()
                nombre_tutor = a.getNombreTutor()
                tlf_tutor = a.getTelefono()
                dni_tutor = a.getDNI()

                item = QTableWidgetItem(nombre_alumno)
                item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
                self.ui.tbl_alumnos.setItem(contador,0,item)

                item = QTableWidgetItem(nombre_tutor)
                item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                self.ui.tbl_alumnos.setItem(contador,1,item)

                item = QTableWidgetItem(str(tlf_tutor))
                item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                self.ui.tbl_alumnos.setItem(contador,2,item)

                item = QTableWidgetItem(str(dni_tutor))
                item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                self.ui.tbl_alumnos.setItem(contador,3,item)

                contador = contador + 1

################ FUNCIONES COLEGIO PESTAÑA CLASES #######################
 
    def añadirClase(self):
        aux = [] #Esto es necesario para la edición, aqui se le pasa una lista vacía
        clase = InputDialog_Clase(aux)
        añadir = clase.exec()
        if añadir == 1:
            curso, letra = clase.getInputs()
            valor = ClaseDAO.añadirClase(curso,letra)
            if valor == True:
                self.setClases()
                self.setTablaClase() ### Para que se muestre la nueva fila añadida en la tabla.
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText("La clase ya estaba anteriormente introducida en el sistema.")
                msg.setWindowTitle("Error")
                msg.exec_()

    def editarClase(self):
        row = self.ui.tbl_clases.currentRow()
        cursoV = self.ui.tbl_clases.item(row, 0)
        letraV = self.ui.tbl_clases.item(row, 1)
        if (cursoV == None) : ### Si no selecciona ninguna fila
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("Debes seleccionar una clase para editarla.")
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            clase_elegida = [cursoV.text(),letraV.text()]
            clase = InputDialog_Clase(clase_elegida)
            editar = clase.exec()
            if editar == 1:
                cursoN, letraN = clase.getInputs()
                valor = ClaseDAO.editarClase(cursoV.text(),letraV.text(),cursoN,letraN)
                if valor == True:
                    self.setClases()
                    self.setTablaClase() # Para que se muestre la nueva fila editada en la tabla.
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText("La clase ya estaba anteriormente introducida en el sistema.")
                    msg.setWindowTitle("Error")
                    msg.exec_()

    def borrarClase(self):
        row = self.ui.tbl_clases.currentRow()
        curso = self.ui.tbl_clases.item(row, 0)
        letra = self.ui.tbl_clases.item(row, 1)
        if(curso == None):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("Debes seleccionar una clase que eliminar.")
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            ClaseDAO.borrarClase(int(curso.text()),letra.text()) # Se borra de la bbdd.
            self.setClases()
            self.setTablaClase() # Para que se muestre la nueva tabla, con el registro borrado.

    def setClases(self):
        self.ui.cb_selgrupo.clear()
        items = ClaseDAO.getClases()
        items_añadir = []
        for i in items:
            items_añadir.append(i.__str__())
        self.ui.cb_selgrupo.addItems(items_añadir)
        self.setTreeColegio()
        self.setTreeGrupos()
    
    def setTablaClase(self):
        self.borrarTabla(self.ui.tbl_clases)
        items = ClaseDAO.getClases()
        contador = 0
        for i in items:
            numRows = self.ui.tbl_clases.rowCount()
            self.ui.tbl_clases.insertRow(contador)
            
            curso = i.getClase()
            clase = i.getLetra()
            num_alumnos = len(AlumnoDAO.getAlumnoPorClase(str(curso)+clase))

            item = QTableWidgetItem(str(curso))
            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.ui.tbl_clases.setItem(contador,0,item)

            item = QTableWidgetItem(clase)
            item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            self.ui.tbl_clases.setItem(contador,1,item)

            item = QTableWidgetItem(str(num_alumnos))
            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.ui.tbl_clases.setItem(contador,2,item)

            contador = contador + 1
    
    def borrarTabla(self,tabla):
        while tabla.rowCount() > 0:
            tabla.removeRow(0)

    def setTreeColegio(self):
        self.ui.treeClases.clear()
        items = ClaseDAO.getClases()
        clases = []
        for i in items:
            clases.append(i.__str__())
        grupos = {}

        grupo = clases[0][0]
        clases_grupo = []
        for i in clases:
            if i[0] != grupo and grupo != "":
                grupos[grupo] = clases_grupo
            #if i[0] not in grupos:
                clases_grupo = []
                grupo = i[0]
                clases_grupo.append(i)
            else:
                clases_grupo.append(i)
        grupos[grupo] = clases_grupo
        
        for grupo,clases in grupos.items():
            parent = QTreeWidgetItem(self.ui.treeClases)
            parent.setText(0,str(grupo)+"º")
            #parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            
            for x in clases:
                child = QTreeWidgetItem(parent)
                #child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0,"{0}".format(x))
                alumnos = AlumnoDAO.getAlumnoPorClase(child.text(0))
                for y in alumnos:
                    childAlumno = QTreeWidgetItem(child)
                    childAlumno.setText(0,y.getNombreAlumno())
                #child.setCheckState(0,Qt.Unchecked)

class InputDialog_Clase(QDialog):
    def __init__(self,clase_elegida, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Datos Clase")
        self.curso = QLineEdit(self)
        self.clase = QLineEdit(self)

        self.onlyInt = QtGui.QIntValidator()
        self.curso.setValidator(self.onlyInt)

        reg_ex = QtCore.QRegExp("[A-Z]")
        input_validator = QtGui.QRegExpValidator(reg_ex,self)
        self.clase.setValidator(input_validator)

        self.curso.setMaxLength(1)
        self.clase.setMaxLength(1)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.setEnabled(False)

        layout = QFormLayout(self)
        layout.addRow("Curso", self.curso)
        layout.addRow("Clase", self.clase)
        layout.addWidget(self.buttonBox)

        if len(clase_elegida) > 0:
            self.curso.setText(str(clase_elegida[0]))
            self.clase.setText(str(clase_elegida[1]))
            self.buttonBox.setEnabled(True)

        self.curso.textChanged.connect(self.comprobarTexto)
        self.clase.textChanged.connect(self.comprobarTexto)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.curso.text(), self.clase.text())

    def comprobarTexto(self):
        if self.curso.text() != "" and self.clase.text() != "":
            self.buttonBox.setEnabled(True)
        else:
            self.buttonBox.setEnabled(False)

class InputDialog_Alumno(QDialog):
    def __init__(self, alumno_elegido, clases, parent=None):
        super().__init__(parent)
        self.clases = clases

        self.setWindowTitle("Datos Alumno")
        self.alumno = QLineEdit(self)
        self.tutor = QLineEdit(self)
        self.telefono = QLineEdit(self)
        self.dni = QLineEdit(self)
        self.elegirClase = QComboBox(self)

        self.elegirClase.addItems(self.clases)

        reg_ex = QtCore.QRegExp("[A-Za-z ]+")
        input_validator = QtGui.QRegExpValidator(reg_ex,self)
        self.alumno.setValidator(input_validator)
        self.tutor.setValidator(input_validator)

        self.onlyInt = QtGui.QIntValidator()
        self.telefono.setValidator(self.onlyInt)

        self.alumno.setMaxLength(30)
        self.tutor.setMaxLength(30)
        self.telefono.setMaxLength(9)
        self.dni.setMaxLength(9)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.setEnabled(False)

        layout = QFormLayout(self)
        layout.addRow("Alumno", self.alumno)
        layout.addRow("Tutor", self.tutor)
        layout.addRow("Tlf.", self.telefono)
        layout.addRow("DNI", self.dni)
        layout.addRow("Clase",self.elegirClase)
        layout.addWidget(self.buttonBox)

        if len(alumno_elegido) > 0:
            self.alumno.setText(str(alumno_elegido[0]))
            self.tutor.setText(str(alumno_elegido[1]))
            self.telefono.setText(str(alumno_elegido[2]))
            self.dni.setText(str(alumno_elegido[3]))
            #self.elegirClase.setText(str(alumno_elegido[1])) 
            self.buttonBox.setEnabled(True)

        self.alumno.textChanged.connect(self.comprobarTexto)
        self.tutor.textChanged.connect(self.comprobarTexto)
        self.telefono.textChanged.connect(self.comprobarTexto)
        self.dni.textChanged.connect(self.comprobarTexto)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.alumno.text(), self.tutor.text(), self.telefono.text(), self.dni.text(),self.elegirClase.currentText())

    def comprobarTexto(self):
        if self.alumno.text() != "" and self.tutor.text() != "" and self.telefono.text() != "" and self.dni.text() != "":
            self.buttonBox.setEnabled(True)
        else:
            self.buttonBox.setEnabled(False)