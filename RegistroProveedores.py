from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QMessageBox, QToolTip
from PyQt5.QtSql import *
import sys, time, pyodbc
from pyodbc import *
Fecha=time.strftime("%x")

Validacion=False
Error=False
class Ui_MainWindow(object):
   
    def __init__(self):
        self.conexionBD=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server};'
                                'SERVER=JEFFERSON-PC;'
                                'DATABASE=MegaMercado;'
                                'Trusted_Connection=yes;')
        print("Base de datos conectada")
        
    def RegistrarProveedorSQL(self, codigo,direccion,nombre,tipo,telefono,RnC,Status):
        cur = self.conexionBD.cursor()
        sql= "INSERT INTO Proveedores1 (Prov_Codigo,Prov_Direccion,Prov_Nombre,Prov_Tipo,Prov_Telefono,Prov_RNC,Prov_Status) Values(?,?,?,?,?,?,?)"
        cur.execute(sql,codigo,direccion,nombre,tipo,telefono,RnC,Status)
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()
        self.radioButton.click()
        self.ventanaExitosa()
        self.obtenerUltimoProv()
        cur.commit()
        cur.close()  

    def EliminaProveedorSql(self,codigo):
        cur = self.conexionBD.cursor()
        sql='''UPDATE Proveedores1 Set Prov_Status='B' WHERE Prov_Codigo = {}'''.format(codigo)
        self.ejecuccionExitosa(sql,cur)
        a = cur.rowcount
        cur.commit()    
        cur.close()
        return a 

    def ActualizarProvSql(self,direccion,nombre,tipo,telefono,RnC,codigo):
        cur= self.conexionBD.cursor()
        sql ='''UPDATE Proveedores1 SET Prov_Direccion = '{}', Prov_Nombre = '{}', Prov_Tipo = '{}', Prov_Telefono= '{}',Prov_RNC= '{}'
        WHERE Prov_Codigo = '{}' '''.format(direccion,nombre,tipo,telefono,RnC,codigo)
        self.ejecuccionExitosa(sql,cur)
        a = cur.rowcount
        cur.commit()    
        cur.close()
        return a  

    def ActualizarProv(self):
        global Validacion
        global Error
        tipo1="" 
        variable=''
        variable1=''
        variable2=''
        Validacion=False
        cur= self.conexionBD.cursor()
        Validacion=False

        if self.radioButton.isChecked() and not self.radioButton_2.isChecked and not self.radioButton_3.isChecked:
                tipo1="Proveedores de productos o bienes"
        elif self.radioButton_2.isChecked() and not self.radioButton.isChecked() and not self.radioButton_3:
                tipo1="Proveedores de servicios"
        else:
                tipo1="Proveedores externos"
        codigo= self.lineEdit_7.text()
        direccion=self.lineEdit_9.text().strip()
        nombre= self.lineEdit_5.text().strip()
        tipo= tipo1
        telefono=self.lineEdit_6.text().strip()
        RnC=self.lineEdit_8.text().strip()
        try: 
                self.VerifacionBorrado(codigo)
                sql="SELECT Prov_RNC from Proveedores1 where Prov_RNC={} and Prov_Codigo<>{}".format(RnC,codigo)
                cur.execute(sql)
                x=cur.fetchall()
                for i in x:
                        variable=(str(i[0]))
                sql1="SELECT Prov_Telefono from Proveedores1 where Prov_Telefono={} and Prov_Codigo<>{}".format(telefono,codigo)
                cur.execute(sql1)
                x=cur.fetchall()
                for i in x:
                        variable1=(str(i[0]))
                sql="SELECT Prov_Codigo from Proveedores1 where Prov_Codigo={}".format(codigo)
                cur.execute(sql)
                x=cur.fetchall()
                for i in x:
                        variable2=(str(i[0]))
                if len(variable2)==0:
                        self.ventanaError2()
                elif variable==self.lineEdit_8.text():
                        self.ventanaError1_1()
                elif (len(self.lineEdit_9.text())==0 or len(self.lineEdit_5.text())==0) :
                        self.ventanaError2()
                elif len(self.lineEdit_6.text())!=10:
                        self.ventanaError3()
                elif len(self.lineEdit_8.text())!=11:
                        self.ventanaError4()
                elif variable1==self.lineEdit_6.text():
                        self.ventanaTelefono()
                        if Validacion:
                                self.ActualizarProvSql(direccion,nombre,tipo,telefono,RnC,codigo)
                        else:
                                pass
                elif Error==False:
                        self.ventanaConfirmacion_1()
                        if Validacion: 
                                self.ActualizarProvSql(direccion,nombre,tipo,telefono,RnC,codigo)
                        else: 
                                pass
                else: 
                        pass
                Error=False
        except pyodbc.ProgrammingError: 
               self.ventanaError2()
        except TypeError:
                self.ventanaError2()
        
    def RegistrarProv(self):
        tipo1=""
        global Validacion
        variable=''
        variable1=''
        variable2=''
        Validacion=True
        cur= self.conexionBD.cursor()
        if self.radioButton.isChecked() and not self.radioButton_2.isChecked and not self.radioButton_3.isChecked:
                tipo1="Proveedores de productos o bienes"
        elif self.radioButton_2.isChecked() and not self.radioButton.isChecked() and not self.radioButton_3:
                tipo1="Proveedores de servicios"
        else:
                tipo1="Proveedores externos"
        codigo= self.lineEdit_7.text().strip()
        direccion= self.lineEdit_9.text().strip()
        nombre= self.lineEdit_5.text().strip()
        tipo= tipo1
        Status='A'
        telefono=self.lineEdit_6.text().strip()
        RnC=self.lineEdit_8.text().strip()
        try:    
                sql="SELECT Prov_RNC from Proveedores1 where Prov_RNC={}".format(RnC)
                cur.execute(sql)
                x=cur.fetchall()
                for i in x:
                        variable=(str(i[0]))

                sql1="SELECT Prov_Telefono from Proveedores1 where Prov_Telefono={}".format(telefono)
                cur.execute(sql1)
                x=cur.fetchall()
                for i in x:
                        variable1=(str(i[0]))

                sql2="SELECT Prov_Codigo from Proveedores1 where Prov_Codigo={}".format(codigo)
                cur.execute(sql2)
                x=cur.fetchall()
                for i in x:
                        variable2=(str(i[0]))
                if variable2==self.lineEdit_7.text():
                        self.ventanaError1()
                elif variable==self.lineEdit_8.text():
                        self.ventanaError1_1()
                elif len(self.lineEdit_6.text())!=10:
                        self.ventanaError3()
                elif len(self.lineEdit_8.text())!=11:
                        self.ventanaError4()
                elif variable1==self.lineEdit_6.text():
                        self.ventanaTelefono()
                        if Validacion:
                                self.RegistrarProveedorSQL(codigo,direccion,nombre,tipo,telefono,RnC,Status) 
                        else:
                                pass
                else:
                        self.RegistrarProveedorSQL(codigo,direccion,nombre,tipo,telefono,RnC,Status) 
        except pyodbc.IntegrityError:
                self.ventanaError1()
        except pyodbc.ProgrammingError:
                self.ventanaError2()

    def EliminiarProveedor(self):
        global Validacion
        global Error
        Validacion=False
        codigo=self.lineEdit_7.text()
        try: 
                self.VerifacionBorrado(codigo)
                if Error==False:
                        self.ventanaConfirmacion()  
                else:
                        pass
                if Validacion:
                        self.EliminaProveedorSql(codigo)
                else: 
                        pass
        except pyodbc.ProgrammingError: 
                self.ventanaError2()
        except TypeError:
                self.ventanaError2()
        Error=False
        
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 599)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1000, 500))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(335, 65, 340, 31))
        self.label.setStyleSheet("font: 0 20pt \"Roboto Mono\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(290, 200, 101, 21))
        self.label_2.setStyleSheet("font: 16pt \"Roboto Mono\";")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(200, 500, 181, 51))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("color:rgb(255, 255, 255);\n"
"background-color: rgb(33, 167, 218);\n"
"font: 63 13pt \"Roboto Mono\";\n"
"font-weight: bold;\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton4 = QtWidgets.QPushButton(self.frame)
        self.pushButton4.setGeometry(QtCore.QRect(600, 500, 181, 51))
        self.pushButton4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton4.setStyleSheet("color:rgb(255, 255, 255);\n"
"background-color: rgb(49, 210, 49);\n"
"font: 63 13pt \"Roboto Mono\";\n"
"font-weight: bold;\n"
"")
        self.pushButton4.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(410, 30, 191, 41))
        self.label_4.setStyleSheet("font: 75 20pt \"Roboto Mono\";\n"
"font-weight: bold")
        self.label_4.setObjectName("label_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_5.setGeometry(QtCore.QRect(390, 200, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto Mono ")
        font.setPointSize(9)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setText("")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(260, 250, 121, 21))
        self.label_5.setStyleSheet("font: 16pt \"Roboto Mono\";")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(230, 300, 171, 21))
        self.label_6.setStyleSheet("font: 16pt \"Roboto Mono\";")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(240, 350, 131, 21))
        self.label_7.setStyleSheet("font: 16pt \"Roboto Mono\";")
        self.label_7.setObjectName("label_7")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_6.setGeometry(QtCore.QRect(390, 250, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto Mono ")
        font.setPointSize(9)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setStyleSheet("")
        self.lineEdit_6.setText("")
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_8.setGeometry(QtCore.QRect(390, 300, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto Mono ")
        font.setPointSize(9)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setStyleSheet("")
        self.lineEdit_8.setText("")
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_9.setGeometry(QtCore.QRect(390, 350, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto Mono ")
        font.setPointSize(9)
        self.lineEdit_9.setFont(font)
        self.lineEdit_9.setStyleSheet("")
        self.lineEdit_9.setText("")
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(400, 500, 181, 51))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("color:rgb(255, 255, 255);\n"
"background-color: rgb(225, 13, 13);\n"
"font: 63 13pt \"Roboto Mono\";\n"
"font-weight: bold;\n"
"")
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setGeometry(QtCore.QRect(300, 410, 131, 31))
        self.label_8.setStyleSheet("font: 16pt \"Roboto Mono\";")
        self.label_8.setObjectName("label_8")
        self.scrollArea = QtWidgets.QScrollArea(self.frame)
        self.scrollArea.setGeometry(QtCore.QRect(380, 390, 271, 81))
        self.scrollArea.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"border-radius: 10px\n"
"")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 271, 81))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton.setGeometry(QtCore.QRect(10, 10, 261, 17))
        self.radioButton.setStyleSheet("font: 9pt \"Roboto Mono\";")
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 30, 211, 17))
        self.radioButton_2.setStyleSheet("font: 9pt \"Roboto Mono\";")
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton_3.setGeometry(QtCore.QRect(10, 50, 181, 17))
        self.radioButton_3.setStyleSheet("font: 9pt \"Roboto Mono\";")
        self.radioButton_3.setObjectName("radioButton_3")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(290, 140, 101, 51))
        self.label_3.setStyleSheet("font: 16pt \"Roboto Mono\";")
        self.label_3.setObjectName("label_3")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_7.setGeometry(QtCore.QRect(390, 150, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto Mono ")
        font.setPointSize(9)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setText("")
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.lineEdit_5, self.pushButton_3)
        MainWindow.setTabOrder(self.pushButton_3, self.lineEdit_6)
        MainWindow.setTabOrder(self.lineEdit_6, self.pushButton)
        MainWindow.setTabOrder(self.pushButton, self.lineEdit_9)
        MainWindow.setTabOrder(self.lineEdit_9, self.lineEdit_8)
        self.lineEdit_5.setMaxLength(50)
        self.lineEdit_6.setMaxLength(10)
        self.lineEdit_8.setMaxLength(11)
        self.lineEdit_9.setMaxLength(70)
        regex = QtCore.QRegExp("[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]*")
        RegEx1= QtCore.QRegExp("[0-9]*")
        validator = QtGui.QRegExpValidator(regex, self.lineEdit_5)
        validatorInt= QtGui.QRegExpValidator(RegEx1, self.lineEdit_6)
        validatorInt2= QtGui.QRegExpValidator(RegEx1, self.lineEdit_8)
        validatorInt3= QtGui.QRegExpValidator(RegEx1, self.lineEdit_7)
        self.lineEdit_5.setValidator(validator)
        self.lineEdit_6.setValidator(validatorInt)
        self.lineEdit_8.setValidator(validatorInt2)
        self.lineEdit_7.setValidator(validatorInt3)

        #BORDE ESTILO
        self.pushButton.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=8, xOffset=0, yOffset=1))
        self.pushButton_3.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=8, xOffset=0, yOffset=1))
        self.pushButton4.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=8, xOffset=0, yOffset=1))
        self.lineEdit_5.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=8, xOffset=0, yOffset=1))
        self.lineEdit_6.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=8, xOffset=0, yOffset=1))
        self.lineEdit_7.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=8, xOffset=0, yOffset=1))
        self.lineEdit_8.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=8, xOffset=0, yOffset=1))
        self.lineEdit_9.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=8, xOffset=0, yOffset=1))
        self.pushButton.clicked.connect(self.RegistrarProv)
        self.pushButton_3.clicked.connect(self.EliminiarProveedor)
        self.pushButton4.clicked.connect(self.ActualizarProv)
        self.fecha = QtWidgets.QLabel(self.frame)
        self.fecha.setGeometry(QtCore.QRect(455, 95, 271, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto Mono")
        font.setPointSize(12)
        self.fecha.setFont(font)
        self.fecha.setText(Fecha)
        self.radioButton.click()
        font = QtGui.QFont()
        font.setFamily("Roboto Mono")
        font.setPointSize(8)
        font.setBold(True)
        self.UltimoProv= QtWidgets.QLabel(self.frame)
        self.UltimoProv.setGeometry(QtCore.QRect(550, 142, 271, 45))
        self.obtenerUltimoProv()
        self.UltimoProv.setFont(font)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Registro de Proveedores"))
        self.label.setText(_translate("MainWindow", "Registro de Proveedor"))
        self.label_2.setText(_translate("MainWindow", "Nombre:"))
        self.pushButton.setText(_translate("MainWindow", "Registrar"))
        self.label_4.setText(_translate("MainWindow", "MEGAMERCADO"))
        self.label_5.setText(_translate("MainWindow", "Telefono:"))
        self.label_6.setText(_translate("MainWindow", "RNC/Cedula:"))
        self.label_7.setText(_translate("MainWindow", "Direccion:"))
        self.pushButton_3.setText(_translate("MainWindow", "Eliminar"))
        self.pushButton4.setText(_translate("MainWindow", "Actualizar"))
        self.label_8.setText(_translate("MainWindow", "Tipo:"))
        self.radioButton.setText(_translate("MainWindow", "Proveedores de productos o bienes"))
        self.radioButton_2.setText(_translate("MainWindow", "Proveedores de servicios"))
        self.radioButton_3.setText(_translate("MainWindow", "Proveedores externos"))
        self.label_3.setText(_translate("MainWindow", "Codigo:"))

    def ventanaError1(self):
                msg= QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("El codigo del proveedor ya existe.")
                msg.setIcon(QMessageBox.Critical)
                msg.setInformativeText("El codigo "+ self.lineEdit_7.text() + " ya esta registrado en la Base de datos.")
                ejecutrMsg=msg.exec_()

    def ventanaError1_1(self):
                msg= QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("El RNC del proveedor ya existe.")
                msg.setIcon(QMessageBox.Critical)
                msg.setInformativeText("El RNC "+ self.lineEdit_8.text() + " ya esta registrado en la Base de datos.")
                ejecutrMsg=msg.exec_()

    def ventanaError2(self):
                msg= QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Error en los datos.")
                msg.setIcon(QMessageBox.Warning)
                msg.setInformativeText("Verifique que los campos no estan vacios o el codigo no existe.")
                ejecutrMsg=msg.exec_()

    def ventanaError3(self):
                msg= QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Error en los datos.")
                msg.setIcon(QMessageBox.Warning)
                msg.setInformativeText("El campo telefono debe de tener 10 digitios")
                ejecutrMsg=msg.exec_()

    def ventanaError4(self):
                msg= QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Error en los datos.")
                msg.setIcon(QMessageBox.Warning)
                msg.setInformativeText("El campo RNC debe de tener 11 digitios")
                ejecutrMsg=msg.exec_()

    def ventanaExitosa(self):
                msg= QMessageBox()
                msg.setWindowTitle("Accion ejectuada")
                msg.setText("La accion ha sido realizada con exito")
                msg.setIcon(QMessageBox.Information)
                ejecutrMsg=msg.exec_()

    def ventanaTelefono(self):
                msg= QMessageBox()
                msg.setWindowTitle("Validacion de accion")
                msg.setText("El telefono "+ self.lineEdit_6.text() + " ya esta registardo ¿Seguro que quiere usar este telefono?")
                msg.setIcon(QMessageBox.Question)
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.buttonClicked.connect(self.ventanaConfButton)
                ejecutrMsg=msg.exec_()

    def ventanaConfirmacion(self):
                msg= QMessageBox()
                msg.setWindowTitle("Validacion de accion")
                msg.setText("¿Estas seguro que deseas eliminar el proveedor de codigo " + self.lineEdit_7.text()+ ", nombre "+ self.ObtenerNombre()
                +" y cedula/RNC "+ self.ObtenerRNC_Cedula()+"?")
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.buttonClicked.connect(self.ventanaConfButton)
                ejecutrMsg=msg.exec_() 

    def ventanaConfirmacion_1(self):
                msg= QMessageBox()
                msg.setWindowTitle("Validacion de accion")
                msg.setText("¿Estas seguro que deseas cambiar los datos del proveedor de codigo " + self.lineEdit_7.text()+ ", nombre "+ self.ObtenerNombre()
                +" y cedula/RNC "+ self.ObtenerRNC_Cedula()+"?")
                msg.setIcon(QMessageBox.Question)
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.buttonClicked.connect(self.ventanaConfButton)
                ejecutrMsg=msg.exec_()

    def ventanaConfButton(self,i):
                global Validacion
                if i.text()=='&Yes':
                        Validacion=True
                else:
                        Validacion=False
    def obtenerUltimoProv(self):
                sql='Select TOP 1 Prov_Codigo from Proveedores1 Order by Prov_Codigo desc'
                cur = self.conexionBD.cursor()
                cur.execute(sql)
                x=cur.fetchall()
                for i in x:
                        return self.UltimoProv.setText('Codigo del ultimo\nproveedor registrado: '+ str(i[0]))
                
    def ObtenerNombre(self):
                codigo=self.lineEdit_7.text()
                cur = self.conexionBD.cursor()
                sql="SELECT Prov_Nombre from Proveedores1 where Prov_Codigo={}".format(codigo)
                try:
                        cur.execute(sql)
                except pyodbc.ProgrammingError:
                        self.ventanaError2()
                x=cur.fetchall()
                for i in x:
                        return str(i[0])
                cur.commit()
                cur.close()
                
    def ObtenerRNC_Cedula(self):
                codigo=self.lineEdit_7.text()
                cur = self.conexionBD.cursor()
                sql="SELECT Prov_RNC from Proveedores1 where Prov_Codigo={}".format(codigo)
                try:
                        cur.execute(sql)
                except pyodbc.ProgrammingError:
                        self.ventanaError2()
                registros= cur.fetchall()
                for i in registros:
                        return str(i[0])
                cur.commit()
                cur.close()

    def VerifacionBorrado(self,codigo):
                var=''
                global Error
                cur=self.conexionBD.cursor()
                sql="SELECT Prov_Status from Proveedores1 where Prov_Codigo={}".format(codigo)
                cur.execute(sql)
                x=cur.fetchall()
                for i in x:
                        var=str(i[0])
                if var=='B':
                        msg= QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setText("El proveedor esta eliminado, no se puede ejecutar la accion")
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec_()
                        Error=True
                        var=''
                else:
                        pass
    def ejecuccionExitosa(self,sql,cur):
                cur.execute(sql)
                self.lineEdit_5.clear()
                self.lineEdit_6.clear()
                self.lineEdit_7.clear()
                self.lineEdit_8.clear()
                self.lineEdit_9.clear()
                self.radioButton.click()
                self.ventanaExitosa()
             
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

