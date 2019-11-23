import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QMessageBox 
import cv2
import matplotlib.pyplot as chang
import HnyFaceDetection
from line_notify import LineNotify
import urllib.request
import os
import shutil

Face_functions = HnyFaceDetection.Face_functions()

class Window(QtGui.QMainWindow):
    def __init__(self):        
        super(Window, self).__init__()
        self.setGeometry(100,100, 720, 480)        
        self.setWindowTitle("Lukhamhanwarinchamrab School")
        self.setWindowIcon(QtGui.QIcon('logo.jpeg'))
        self.setFixedSize(720, 480)
        self.home()   
        
    def home(self):
        newfont = QtGui.QFont("RSU", 16, QtGui.QFont.Bold)       

        self.result = QtGui.QLabel(self)
        self.result.setText("-")
        self.result.setFont(newfont)
        self.result.setGeometry(890,750,500,20)
        
        self.state = QtGui.QLabel(self)
        self.state.setText("ID :")
        self.state.setFont(newfont)
        self.state.setGeometry(460,45,80,30)
       
        self.id_box = QtGui.QLineEdit(self)
        self.id_box.resize(100,25)
        self.id_box.move(570,50)
        self.id_box.setText("")
        
        self.state = QtGui.QLabel(self)
        self.state.setText("Name :")
        self.state.setFont(newfont)
        self.state.setGeometry(460,85,120,30)
       
        self.id_name = QtGui.QLineEdit(self)
        self.id_name.resize(100,25)
        self.id_name.move(570,90)
        self.id_name.setText("")
                
        self.connect_state = QtGui.QLabel(self)
        if(self.connect()):
            self.connect_state.setStyleSheet('color:green; border: 2px solid green')
            self.connect_state.setText("Online!") 
        else:
            self.connect_state.setStyleSheet('color:red; border: 2px solid red')
            self.connect_state.setText("Offline!")
        self.connect_state.setGeometry(650,450,70,30)
      
        self.state_view = QtGui.QLabel(self)
        self.state_view.setText("Welcome")
        self.state_view.setStyleSheet('color:blue')
        self.state_view.setGeometry(460,120,250,30)
     
        #--------------- set position preview ---------------------------------------
                
        width2 = 400
        height2 = 400
        self.picc = QtGui.QLabel(self)
        self.picc.setGeometry(800, 50,  640, 480)
                
        self.picc1 = QtGui.QLabel(self)
        self.picc1.setGeometry(150, 50,  width2, height2)
        #self.picc1.setPixmap(pix2)       
       
        #---------------------------BUTTON-------------------------------------

        btn_register = QtGui.QPushButton("Register",self)
        btn_register.clicked.connect(self.actions_Register)
        btn_register.resize(400,100)
        btn_register.move(50,50)
        
        btn_update = QtGui.QPushButton("Update", self)
        btn_update.clicked.connect(self.actions_update)
        btn_update.resize(400,100)
        btn_update.move(50,170)
            
        btn_start = QtGui.QPushButton("Start", self)
        btn_start.clicked.connect(self.actions_start)
        btn_start.resize(400,100)
        btn_start.move(50,290)
        
        clear_data = QtGui.QPushButton("Remove", self)
        clear_data.clicked.connect(self.action_remove_data)
        clear_data.resize(70,50)
        clear_data.move(50,400)

        self.show()
    
    #----------------------------------ACTION FUNCTIONS---------------------------
    def actions_Register(self):
        Face_functions.Start_get_data(self.id_box.text(),self.id_name.text())
        self.state_view.setText("Add member to database already.")
        #print(self.id_box.text())
        
    def actions_start(self):
        Face_functions.scan_run()
        self.state_view.setText("Program is running.")
        
    def actions_update(self):
        token = '7w9sX5x78568L8lCGQ27hfvEyXPfzxZF2orUcCavcJ2'
        notify  = LineNotify(token)
        notify.send('Upadate Data already')
        self.state_view.setText("Update data base complete.")
        Face_functions.trainModel()
        
    def action_remove_data(self):
        shutil.rmtree('dataset',ignore_errors = True)
        try:
            os.remove('database.npy')
        except:
            return 1
        os.makedirs('dataset')
        self.state_view.setText("Remove database complete.")
        

    def cvt_image(self,photo,width,height):        
        picx = cv2.imread(photo)
        dim = (width, height)
        pic1 = cv2.resize(picx, dim, interpolation = cv2.INTER_AREA)
        image = QtGui.QImage(pic1, pic1.shape[1],pic1.shape[0], pic1.shape[1] * 3,QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(image)
      
        return pix,width,height

    
    
    def connect(self,host='http://google.com'):
        try:
            urllib.request.urlopen(host)
            return True
        except:
            return False       
        

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()

