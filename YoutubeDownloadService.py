from pytube import YouTube
import os
import re
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt




save_dir='./'

class YoutubeDownload(QDialog):
    def __init__(self,parent=None):
        # super(YoutubeDownload,self).__init__()
        super().__init__(parent)
        loadUi("./UI_File/downloader.ui",self)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.Intialrun(save_dir)
        self.FilesList.setReadOnly(True)
        self.BTNDownloder.clicked.connect(self.fetchurandsendforDownload)


    def Intialrun(self,save_dir,newfilename=None):
        if os.path.exists(save_dir) and os.path.isdir(save_dir):
            files = [f for f in os.listdir(save_dir) if os.path.isfile(os.path.join(save_dir, f))]
            if not len(files) > 0:
                self.Dir_List.setText("Current Directory Doesn't Have File To Display")
            else:
                self.Dir_List.setText("List Of The Files Present in Current Directory")
                for index,file in enumerate(os.listdir(save_dir)):
                    self.FilesList.append(f"{str(index+1)}:{file}")
                    self.FilesList.append('________________________________')



    def fetchurandsendforDownload(self):
        self.MessageFiled.setText("Please Wait...Url is Beening Checked For Downloading")
        QApplication.processEvents()
        URL=self.URLField.text()

        url_pattern = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")
        if re.match(url_pattern, URL):
            self.download_youtube_video (URL)     
        else:
            self.MessageFiled.setText("Please Enter Valid URL")
        
        


    def download_youtube_video(self,video_url):  
        
        try:
            self.MessageFiled.setText("Please Wait... Downloading")
            QApplication.processEvents()
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=save_dir)
            file_name = stream.default_filename
            self.MessageFiled.setText(f"Downloded File : --->{file_name}<---- You Can Seen Below")
        except Exception as e:
            self.MessageFiled.setText("Due To Some Technical Issues This Video Can't Be Downloaded")
                    
        self.FilesList.clear()
        self.Intialrun(save_dir)
