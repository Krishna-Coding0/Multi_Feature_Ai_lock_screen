from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

from transformers import pipeline



class text_Summarization(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        loadUi("./UI_File/textSummarization.ui",self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        intvalidator=QIntValidator()
        self.textsummerizationlenght.setValidator(intvalidator)
        self.BTNtextsummarization.clicked.connect(self.gptworking)

    def gptworking(self):
        self.llmlabel.setText('Wait Summarized Text is Being Genrated')
        QApplication.processEvents()
        ARTICLE = self.entertext.toPlainText()
        maxlength = int(self.textsummerizationlenght.text())
        try:
            if maxlength>=20:
                sumri_text=self.summarizer(ARTICLE, max_length=maxlength, min_length=10, do_sample=False)
                self.textsummerizationinputfield.setText(sumri_text[0]['summary_text'])
                self.llmlabel.setText('Text is Genrated ')
            else:
                self.llmlabel.setText('Max Token is Less Then Min Tokens')
        except:
            self.llmlabel.setText('Due To Some Problem System is Not Working')

