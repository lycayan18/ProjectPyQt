import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QInputDialog, QMainWindow, QMessageBox
import requests
import csv
from googletrans import Translator
from pprint import pprint
from datetime import datetime


class MyWidget(QMainWindow):

    def __init__(self):
        global widget
        super().__init__()
        uic.loadUi('Main2.ui', self)

        self.trans = Translator()

        self.open_weather_token = 'e201b2ce51d9eda6f6dcc27e9bb9fbb9'

        self.country, ok_pressed1 = QInputDialog.getText(self, "Выбор страны",
                                                         "Пожалуйста введите название страны")

        if ok_pressed1:
            self.city, ok_pressed2 = QInputDialog.getText(self, "Выбор города",
                                                          "Пожалуйста введите название города")
        if ok_pressed2:
            self.get_weather()

    def get_weather(self):
        try:
            self.country = self.trans.translate(self.country, src='ru', dest='en').text

            with open('all.csv') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                for index, row in enumerate(reader):
                    if row[0] == self.country:
                        self.iso = row[4]
                        self.iso = self.iso[-1:-3]
                        break

            r1 = requests.get(
                f"http://api.openweathermap.org/geo/1.0/direct?q={self.city},{self.iso}&limit={1}&appid={self.open_weather_token}"
            )
            self.data1 = r1.json()
            self.data1 = self.data1[0]
            self.lat = self.data1['lat']
            self.lon = self.data1['lon']
            r2 = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.open_weather_token}&units={'metric'}&lang={'ru'}"
            )
            self.data = r2.json()
            self.show_weather()
        except Exception:
            self.error = QMessageBox()
            self.error.setWindowTitle('Ошибка')
            self.error.setText('Пожалуйста убедитесь в верности написания!')
            self.error.setStandardButtons(QMessageBox.Ok)
            self.error.buttonClicked.connect(self.errors)
            self.error.exec_()

    def errors(self, btn):
        if btn.text() == 'OK':
            self.country, ok_pressed1 = QInputDialog.getText(self, "Выбор страны",
                                                             "Пожалуйста введите название страны")
            if ok_pressed1:
                self.city, ok_pressed2 = QInputDialog.getText(self, "Выбор города",
                                                              "Пожалуйста введите название города")
            if ok_pressed2:
                self.get_weather()

    def show_weather(self):
        self.time = datetime.today().strftime('%H:%M')
        self.degrees = str(int(self.data['main']['temp'])) + '°'
        self.feels_like = 'Ощущается как ' + str(int(self.data['main']['feels_like'])) + '°'
        self.weather = self.data['weather'][0]['description']
        self.wind = 'Ветер - ' + str(self.data['wind']['speed']) + ' м/с'
        self.humidity = 'Влажность - ' + str(self.data['main']['humidity']) + '%'
        self.sunrise = 'Рассвет - ' + str(datetime.fromtimestamp(self.data['sys']['sunrise']).strftime('%H:%M'))
        self.sunset = 'Закат - ' + str(datetime.fromtimestamp(self.data['sys']['sunset']).strftime('%H:%M'))

        text_date_time = self.city + '. Погода на ' + str(self.time)
        self.label_date_time.setText(text_date_time)
        self.label_degrees.setText(self.degrees)
        self.label_weather.setText(self.weather)
        self.label_degrees_of_feeling.setText(self.feels_like)

        self.label_wind.setText(self.wind)
        self.label_humidity.setText(self.humidity)
        self.label_sunrise.setText(self.sunrise)
        self.label_sunset.setText(self.sunset)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())