import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QInputDialog, QMainWindow
import requests
import csv
from bs4 import BeautifulSoup


class MyWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('Main2.ui', self)

        self.town_name, ok_pressed = QInputDialog.getText(self, "Выбор города",
                                                "Пожалуйста введите название города")

        if ok_pressed:
            self.show_the_weather()

    def show_the_weather(self):
        with open('koord_russia.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for index, row in enumerate(reader):
                if row[0] == self.town_name:
                    width = row[-2]
                    longitude = row[-1]
                    print(width, longitude)
                    print(row[0])
                    break
        width = str(width).split(',')
        width = '.'.join(width)
        longitude = str(longitude).split(',')
        longitude = '.'.join(longitude)
        text_url = 'https://yandex.ru/pogoda/?lat=' + width + '&lon=' + longitude + '&via=srp'
        print(text_url)
        url = text_url
        response = requests.get(url)
        bs = BeautifulSoup(response.text, 'lxml')

        self.town = bs.find('h1', class_='title title_level_1 header-title__title').text
        self.time = bs.find('time', class_='time fact__time').text[7:12]
        self.degrees = bs.find('div', class_='temp fact__temp fact__temp_size_s').text
        self.degrees_of_feeling = bs.find('div', class_='term term_orient_h fact__feels-like').text
        self.weather = bs.find('div', class_='link__condition day-anchor i-bem').text

        self.wind = 'Ветер - ' + bs.find('div', class_='term term_orient_v fact__wind-speed').find('div', class_='term__value').text
        self.humidity = 'Влажность - ' + bs.find('div', class_='term term_orient_v fact__humidity').text[:3]
        self.sunrise = bs.find('div', class_='sun-card__sunrise-sunset-info sun-card__sunrise-sunset-info_value_rise-time').text[:6] + \
                       ' - ' + bs.find('div', class_='sun-card__sunrise-sunset-info sun-card__sunrise-sunset-info_value_rise-time').text[6:]
        self.sunset = bs.find('div', class_='sun-card__sunrise-sunset-info sun-card__sunrise-sunset-info_value_set-time').text[:5] + \
                       ' - ' + bs.find('div', class_='sun-card__sunrise-sunset-info sun-card__sunrise-sunset-info_value_set-time').text[5:]

        text_date_time = self.town + '. Погода на ' + self.time
        self.label_date_time.setText(text_date_time)
        self.label_degrees.setText(self.degrees)
        self.label_weather.setText(self.weather)
        self.label_degrees_of_feeling.setText(self.degrees_of_feeling)

        self.label_wind.setText(self.wind)
        self.label_humidity.setText(self.humidity)
        self.label_sunrise.setText(self.sunrise)
        self.label_sunset.setText(self.sunset)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())