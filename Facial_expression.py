import uuid
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
import tensorflow as tf
import warnings
import pickle

warnings.filterwarnings('ignore')
model = tf.keras.models.load_model('./Modelfile/facialEmotion.h5')

with open('./Modelfile/label_encoder.pkl', 'rb') as f:
    le = pickle.load(f)


class FacialExpression(QDialog):
    def __init__(self):
        super(FacialExpression,self).__init__()
        loadUi("./UI_File/Facial.ui",self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.BTNCaptureFacial.clicked.connect(self.capture_image)  
        self.camera()


    def camera(self):
        # self.Registerlabel.setText("Click on Upload")
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
                self.FaceArea.setPixmap(QPixmap.fromImage(q_img))

    def capture_image(self):
        self.PredictedLabel.setText('Please Wait a While.......')
        QApplication.processEvents()
        ret, frame = self.capture.read()
        if not ret:
            print("Failed to capture frame from camera.")
            return
        
        file_name = str(uuid.uuid1()) + '.jpg'
        file_name_path = './output/' + file_name
        
        if cv2.imwrite(file_name_path, frame):
            print("Image saved as:", file_name_path)
            
            custom_image = cv2.imread(file_name_path, cv2.IMREAD_GRAYSCALE)
            if custom_image is None:
                print("Failed to read the captured image.")
                return
            
            resized_custom_image = cv2.resize(custom_image, (48, 48))
            custom_image_input = resized_custom_image.reshape((1, 48, 48, 1))
            
            pred = model.predict(custom_image_input)
            prediction_label = le.inverse_transform([pred.argmax()])[0]
            self.PredictedLabel.setText(f'Predicted Expression :{prediction_label}')
            print("Predicted Output:", prediction_label)
        else:
            print("Failed to save captured image.")

        
        self.capture.release()
        cv2.destroyAllWindows()
        self.timer.timeout.disconnect(self.display_frame)  
        self.timer.stop()



