from PyQt5.QtCore import QUrl, Qt, QCoreApplication
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Set the attribute before creating QApplication instance

class WebBrowser(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("./UI_File/Browser.ui", self)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.verticalLayout.addWidget(self.browser)
        self.EnterURLForWebBrowser.returnPressed.connect(self.navigate_to_url)
        self.BTNForward.clicked.connect(self.browser.forward)
        self.BTNBack.clicked.connect(self.browser.back)
        self.BTNReload.clicked.connect(self.browser.reload)

    def navigate_to_url(self):
        url = self.EnterURLForWebBrowser.text()
        if not url.startswith('http'):
            url = 'http://' + url
        self.browser.setUrl(QUrl(url))
