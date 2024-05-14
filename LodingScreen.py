import sys
import atexit
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
import importlib

import multiprocessing



class LockScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lock Screen")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # Make window stay on top and frameless
        self.setGeometry(0, 0, QApplication.desktop().screenGeometry().width(), QApplication.desktop().screenGeometry().height())  # Set window 

    def closeEvent(self, event):
        event.ignore()  # Ignore the close event

    def mousePressEvent(self, event):
        # Allow mouse clicks to be processed
        super().mousePressEvent(event)

def cleanup():
    # Disable Ctrl+C termination
    sys.stderr = open('error.log', 'a')  # Redirect error messages to a log file

def main_one():
    app = QApplication(sys.argv)

    lock_screen = LockScreen()
    lock_screen.showFullScreen()

    # Register cleanup function
    atexit.register(cleanup)

    sys.exit(app.exec_())

def main_twotwo():
        getattr(importlib.import_module('Main_front'), 'main_two')()


# p1=multiprocessing.Process(target=main_one)
# p2=multiprocessing.Process(target=main_twotwo)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    p1 = multiprocessing.Process(target=main_one)
    p2 = multiprocessing.Process(target=main_twotwo)
    
    p1.start()
    p2.start()
    p1.join(16)  # Wait for p1 to finish or 10 seconds
    if p1.is_alive():
        p1.terminate()  # If p1 is still running after 10 seconds, terminate it
    
    p2.join()  # Wait for p2 to finish or 10 seconds
    
    # if p2.is_alive():
    #     p2.terminate()