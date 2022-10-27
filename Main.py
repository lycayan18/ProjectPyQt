import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QInputDialog, QMainWindow, QMessageBox
import requests
import csv
from googletrans import Translator
from pprint import pprint
from datetime import datetime
from bs4 import BeautifulSoup


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
                        self.iso = self.iso[-2:]
                        break
            r1 = requests.get(
                f"http://api.openweathermap.org/geo/1.0/direct?q={self.city},{self.country}&limit={1}&appid={self.open_weather_token}"
            )
            self.data1 = r1.json()
            self.data1 = self.data1[0]
            self.lat = self.data1['lat']
            self.lon = self.data1['lon']
            response = requests.get(
                f"https://yandex.ru/pogoda/?lat={self.lat}&lon={self.lon}"
            )
            self.bs = BeautifulSoup(response.text, 'lxml')
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
        self.city = self.bs.find('h1', class_='title title_level_1 header-title__title').text
        self.time = self.bs.find('time', class_='time fact__time').text[7:12]
        self.degrees = self.bs.find('span', class_='temp__value temp__value_with-unit').text
        self.feels_like = 'Ощущается как ' + self.bs.find('span', class_='temp__value temp__value_with-unit').text
        self.weather = self.bs.find('div', class_='link__condition day-anchor i-bem').text
        self.wind = 'Ветер - ' + self.bs.find('div', class_='term term_orient_v fact__wind-speed').find('div', class_='term__value').text
        self.humidity = 'Влажность - ' + self.bs.find('div', class_='term term_orient_v fact__humidity').text[:3]
        self.sunrise = self.bs.find('div', class_='sun-card__sunrise-sunset-info sun-card__sunrise-sunset-info_value_rise-time').text[:6] + \
                       ' - ' + self.bs.find('div', class_='sun-card__sunrise-sunset-info sun-card__sunrise-sunset-info_value_rise-time').text[6:]
        self.sunset = self.bs.find('div', class_='sun-card__sunrise-sunset-info sun-card__sunrise-sunset-info_value_set-time').text[:5] + \
                      ' - ' + self.bs.find('div', class_='sun-card__sunrise-sunset-info sun-card__sunrise-sunset-info_value_set-time').text[5:]
        print(self.degrees)

        text_date_time = self.city + '. Погода на ' + self.time
        self.label_date_time.setText(text_date_time)
        self.label_degrees.setText(self.degrees)
        self.label_weather.setText(self.weather)
        self.label_degrees_of_feeling.setText(self.feels_like)
        print(text_date_time)
        self.label_wind.setText(self.wind)
        self.label_humidity.setText(self.humidity)
        self.label_sunrise.setText(self.sunrise)
        self.label_sunset.setText(self.sunset)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())