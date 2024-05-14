import requests
from PyQt5.QtWidgets import  QDialog
from PyQt5.uic import loadUi
import pickle
import pandas as pd
from PyQt5.QtCore import Qt


class TemperatureClass(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        loadUi("./UI_File/weather.ui",self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.BTNFetchCurrentData.clicked.connect(self.fetch_weather_dataAPI)
        self.SubmitQueryofWaether.clicked.connect(self.fetchdata)
    def fetchdata(self):
        try:
            windedit=self.windedit.text()
            pressureedit=self.pressureedit.text()
            precipedit=self.precipedit.text()
            humidityedit=self.humidityedit.text()
            cloudedit=self.cloudedit.text()

            data={
                'latitude':[23.3441],
                'longitude':[85.3096],
                'wind_kph':[windedit],
                'pressure_mb':[pressureedit],
                'precip_in':[precipedit],
                'humidity':[humidityedit],
                'cloud':[cloudedit]

            }
            dataset=pd.DataFrame(data=data)

            with open('./Modelfile/TemparturePredition.pkl', 'rb') as file:
                model = pickle.load(file)
            op=model.predict(dataset)
            self.outputlabel.setText(f'Temp:{op[0]}')
        except:
            print('Error')

    def fetch_weather_dataAPI(self):
        try:
            api_key = '286f8ebd8433421793d153813241803'
            city = 'RANCHI'
            url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json()['current']
        except:
            print('Error')
        
        self.labelwind_kph.setText( str(data['wind_kph']))
        self.labelpressure_mb.setText(str(data['pressure_mb']))
        self.labelprecip_in.setText(str(data['precip_in']))
        self.labelhumidity.setText(str(data['humidity']))
        self.labelcloud.setText(str(data['cloud']))
        # temp_c = data['temp_c']








