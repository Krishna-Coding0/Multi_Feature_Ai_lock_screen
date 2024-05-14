import cv2
import os
import uuid
import sys
import importlib
import atexit

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication,QHBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer,Qt,QRegExp
from PyQt5.QtGui import QImage, QPixmap,QRegExpValidator,QIntValidator


import Joke_Qoute
import Get_Time_and_Date
import Databasefile.database as dbs





""" Main Class Of The Screen """
class MainWindow(QDialog):

    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("./UI_File/MYFrontEnd.ui",self)
    

        self.valueforverification=False
        self.TextAreaofChat.setReadOnly(True)
        self.BTN_gottoWindow.setEnabled(False)  

        hbox_input = QHBoxLayout()
        hbox_input.addWidget(self.SendingChatToBotText)
        self.verticalLayout.addLayout(hbox_input)

        self.Joke_Quotes()
        self.BTNlogin.clicked.connect(self.checklogincreditial)
        self.BTN_services.setEnabled(False)


        self.BTNNewUser.clicked.connect(self.gotoregistrationpage)
        self.VerifyBTN.clicked.connect(self.camera)
        self.BTN_gottoWindow.clicked.connect(self.existwindow)
        self.SendingChatToBotText.returnPressed.connect(self.send_message)
        self.BTM_For_Send_Msg.clicked.connect(self.send_message)
        QApplication.processEvents()
        self.model,self.universal,self.face_clasifier=self.modelimport()
        
    def modelimport(self):
        myface=getattr(importlib.import_module('facemodelCv'), 'myface')
        model,universal,face_clasifier=myface()
        return model,universal,face_clasifier

    def closeEvent(self, event):
        # Ignore the close event
        event.ignore()  

    def mousePressEvent(self, event):
        # Allow mouse clicks to be processed
        super().mousePressEvent(event)

    def contextMenuEvent(self, event):
        # Disable right-click menu
        event.ignore()

    def keyPressEvent(self, event):
        # Disable escape button
        if event.key() == Qt.Key_Escape:
            event.ignore()


    def checklogincreditial(self):
        dbs=importlib.import_module('Databasefile.database')

        logindata=self.LoginuserCrediential.text()
        # print(logindata)
        if logindata!='':
            status=dbs.fetch_DB_DATA(logindata)
            if status:
                self.TimeandIntoText.setText('You Are in Our Database , You can Use Services')
                self.BTNNewUser.setEnabled(False)
                self.serviceEnable()
                if logindata=='k2':
                    self.BTN_gottoWindow.setEnabled(True)
                    self.VerifyBTN.setEnabled(False)
                    self.BTNlogin.setEnabled(False)
                    self.BTNNewUser.setEnabled(False)
            else:
                self.TimeandIntoText.setText('Please Sign Up Then Try To Login')
        else:
            self.TimeandIntoText.setText('Please Enter Your Username !')


    def serviceEnable(self):
        self.BTN_services.setEnabled(True)
        self.BTN_services.clicked.connect(self.gotoservicepage)

    def existwindow(self):
        sys.exit()




    def gotoregistrationpage(self):
        registers = register_page()
        self.hide()
        registers.exec_()
        self.show()
    def gotoservicepage(self):
        servicepage=Servicepage()
        widget.addWidget(servicepage)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        # widget.setCurrentIndex(1)


    """ chatbot """
    def send_message(self):

        main=getattr(importlib.import_module('Chatbot'), 'main')

        message = self.SendingChatToBotText.text()
        if message:
            self.SendingChatToBotText.clear()
            self.TextAreaofChat.append("User: " + message)  # Display user's message
            
            response = main(message)
            self.TextAreaofChat.append("Bot: " + response)  # Display bot's response



    """ camera Details """

    
    def camera(self):

        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_frame)
        self.timer.start(10)
        
    def display_frame(self):
        ret, frame = self.capture.read() 
        # If frame is successfully read
        if ret:  
            # Convert frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            # Create QImage from frame
            q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)  
            self.ImageDisplayArea.setPixmap(QPixmap.fromImage(q_img))
            # Display QImage on QLabel
        try:
            image,face=self.face_detector(frame)
            faces=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
            result=self.model.predict(faces)

            if result[1]<500:
                confidence=int(100*(1-(result[1])/300))  

            if confidence>75:
                self.destroycamera()
                self.TimeandIntoText.setText('Hello K2 Sir')
                self.BTN_gottoWindow.setEnabled(True) 
                self.VerifyBTN.setEnabled(False)
                self.BTNNewUser.setEnabled(False)
                self.serviceEnable()
            else:
                self.destroycamera()
                self.VerifyBTN.setEnabled(False)
                self.TimeandIntoText.setText('You Must Be New User')
        except:
            self.display_frame()

    def face_detector(self,img,size=0.5):
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=self.face_clasifier.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)

        if faces is():
            return img,[]
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            # roi=region of intrest
            roi=img[y:y+h,x:x+w]
            roi=cv2.resize(roi,(200,200))
        return img,roi


    def destroycamera(self):
            self.capture.release()
            cv2.destroyAllWindows()
            self.timer.timeout.disconnect(self.display_frame)  # Disconnect timer
            self.timer.stop()
    """ end of camera """

    
    def Joke_Quotes(self):
        joke=Joke_Qoute.fetch_joke()
        self.JokeTextArea.setText(joke)
        quote,author=Joke_Qoute.fetch_motivation()
        self.QuoteTextField.setText(quote)
        self.Authorlabel.setText(f'By:{author}')

    def greeting_text_voice(self):
        date_str, day_str, time_str,greetText=Get_Time_and_Date.get_current_datetime()
        self.GreetingText.setText(greetText)



""" Service Page Class and Function """
class Servicepage(QDialog):
    def __init__(self):
        super(Servicepage,self).__init__()
        loadUi("./UI_File/ServiceUI.ui",self)
        self.BTNBack.clicked.connect(self.gotoMainScreen)

        self.BTNdownloder.clicked.connect(self.Youtube)
        self.BTNBrowser.clicked.connect(self.Browser)
        self.BTNDisease.clicked.connect(self.diseases_prediction)
        self.BTNTemperaturePre.clicked.connect(self.TemperatureCalling)
        self.BTNFaceExxpservice.clicked.connect(self.facialexp)
        self.BTNTextSummzarization.clicked.connect(self.textsummarization)
    def gotoMainScreen(self):
        widget.setCurrentIndex(widget.currentIndex() -1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            event.ignore()  # Ignore the escape key press
        else:
            super().keyPressEvent(event)
            
    def Youtube(self):
        self.servicienotice.setText('Please Wait...')
        QApplication.processEvents()
        yt=getattr(importlib.import_module('YoutubeDownloadService'), 'YoutubeDownload')()
        QApplication.processEvents()
        self.servicienotice.setText('')
        if yt.exec_():
            print('Running')
    
    def Browser(self):
        self.servicienotice.setText('Please Wait...')
        QApplication.processEvents()
        wb=getattr(importlib.import_module('OwnBrowser'), 'WebBrowser')()
        QApplication.processEvents()
        self.servicienotice.setText('')
        if wb.exec_():
            print('Running')
        

            
    def diseases_prediction(self):
        self.servicienotice.setText('Please Wait...')
        QApplication.processEvents()
        ds=getattr(importlib.import_module('Diseases'), 'Diseases_class')()
        QApplication.processEvents()
        self.servicienotice.setText('')
        if ds.exec_():
            print('Running')
    
    def TemperatureCalling(self):
        self.servicienotice.setText('Please Wait...')
        QApplication.processEvents()
        tp=getattr(importlib.import_module('TemperatureFile'), 'TemperatureClass')()
        QApplication.processEvents()
        self.servicienotice.setText('')
        if tp.exec_():
            print('Running')
    
    def facialexp(self):
        self.servicienotice.setText('Please Wait...')
        QApplication.processEvents()
        cc=getattr(importlib.import_module('Facial_expression'), 'FacialExpression')()
        QApplication.processEvents()
        self.servicienotice.setText('')
        if cc.exec_():
            print('Running')
            
    def textsummarization(self):
        self.servicienotice.setText('Please Wait...')
        QApplication.processEvents()
        ts=getattr(importlib.import_module('textsummariz'), 'text_Summarization')()
        QApplication.processEvents()
        self.servicienotice.setText('')
        if ts.exec_():
            print('Running')






""" Regitartion Page """
class register_page(QDialog):
    def __init__(self):
        super(register_page,self).__init__()
        loadUi("./UI_File/RegistrationPageUI.ui",self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)



        email_regex = QRegExp("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$") 
        name_regex = QRegExp("^[a-zA-Z]+ [a-zA-Z]+$") 
        email_validator = QRegExpValidator(email_regex)
        alphabet_validator = QRegExpValidator(name_regex)
        intvalidator=QIntValidator()
        self.Addressfield.setValidator(alphabet_validator)
        self.NameField.setValidator(alphabet_validator)
        self.Emailfield.setValidator(email_validator)
        self.Phonefield.setValidator(intvalidator)




        self.BTNregistration.clicked.connect(self.fetch_front_end_data)
        # print(self.BTNregistration.pressed()
        self.Goback.clicked.connect(self.gotoMainScreen)
    
        self.BTNupload.clicked.connect(self.capture_image)  
        # self.BTNupload.setEnabled(False)


    def gotoMainScreen(self):
        self.close()

    def fetch_front_end_data(self):

        self.name=self.NameField.text()
        self.email=self.Emailfield.text()
        self.phno=self.Phonefield.text()
        self.address=self.Addressfield.text()
        self.username=self.UsernameField.text()
        self.checkbox=None
        if self.MaleRadioBTN.isChecked():
            self.checkbox=self.MaleRadioBTN.text()
        elif self.FemaleRadioBTN.isChecked():
            self.checkbox=self.FemaleRadioBTN.text()
        else:
            pass

        if self.name !='' or self.email !='' or self.phno !='' or self.address !='' or self.username !='' or self.checkbox!=None:
            self.NameField.clear()
            self.Emailfield.clear()
            self.Phonefield.clear()
            self.UsernameField.clear()
            self.MaleRadioBTN.setChecked(False)
            self.FemaleRadioBTN.setChecked(False)
            self.Addressfield.clear()
            self.Registerlabel.setText("You Have Regitered ,Now Wait Few Second Then Click on Upload Pic")
            self.camera()



    def camera(self):
        self.Registerlabel.setText("Click on Upload")
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_frame)
        self.timer.start(30)
    def display_frame(self):
        ret, frame = self.capture.read()  # Read frame from webcam
        if ret: 
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB format
                h, w, ch = frame_rgb.shape
                bytes_per_line = ch * w
                q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)  # Create QImage from frame
                self.FacedetCap.setPixmap(QPixmap.fromImage(q_img))

    def capture_image(self):
        ret, frame = self.capture.read()
        file_name_path='./Modelfile/NewUserImg/'+str(uuid.uuid1())+'.jpg'
        if ret:
            cv2.imwrite(file_name_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            print("Image captured!")
        self.Registerlabel.setText("You are Registered")
        
        self.capture.release()
        cv2.destroyAllWindows()
        self.timer.timeout.disconnect(self.display_frame)  # Disconnect timer
        self.timer.stop()
        self.savetodatabase(self.name,self.email,self.phno,self.address,self.username,self.checkbox)


    def savetodatabase(self,name,email,phno,address,username,checkbox):
        filepath=None
        path='Modelfile/NewUserImg/'
        for file in os.listdir(path):
            filepath=os.path.join(path,file)
        value=dbs.storeData(name,email,phno,address,username,checkbox,filepath)
        if value:
            for file in os.listdir(path):
                filepath=os.path.join(path,file)
                os.remove(filepath)


def cleanup():
    sys.stderr = open('error.log', 'a') 

app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
mainwindow=MainWindow()
widget.addWidget(mainwindow)
widget.showFullScreen()
atexit.register(cleanup)
# widget.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint) 
widget.setGeometry(0, 0, QApplication.desktop().screenGeometry().width(),QApplication.desktop().screenGeometry().height()) 


widget.show()
sys.exit(app.exec_())


