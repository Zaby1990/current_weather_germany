import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QPushButton, QGridLayout, QComboBox, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from urllib.request import urlopen
import re
import json

Station_Number = 105770


def read_weather_stations():
    try:
        c = urlopen('http://wetterstationen.meteomedia.de/', timeout=1)
        a = str(c.read(), 'utf-8')
        with open('html_old.txt', 'w') as i:
            i.write(a)

        a1 = a.split('\n')
        ai1 = a1.index('<map name="Karte">')+1
        ai2 = a1.index('</map>')
        Stationen = dict()
        for i in a1[ai1:ai2]:
            stat_no = re.search('[0-9]{6}', i).group()
            stat_name = i[re.search('title="', i).span()[1]:re.search('">', i).span()[0]].replace('&Auml;', 'Ä').replace(
                '&Ouml;', 'Ö').replace('&Uuml;', 'Ü').replace('&auml;', 'ä').replace('&ouml;', 'ö').replace('&uuml;', 'ü').replace('&szlig;', 'ß')
            Stationen[stat_name] = stat_no
        worked = True
    except Exception as e:
        # print(e)
        Stationen = preset['Stationsliste']
        worked = False
    return Stationen, worked


class App(QWidget):
    def __init__(self, Stationen, preset):
        super().__init__()
        self.title = 'Wetter'
        self.left = 1700
        self.top = 100
        self.width = 640
        self.height = 480
        self.Stationen = Stationen
        self.preset = preset
        self.gen_labels()
        self.initUI()

    def gen_labels(self):
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        # DropDownMenue
        self.Drop = QComboBox(self)
        for i in self.Stationen[0].keys():
            self.Drop.addItem(i)
        # Buttons
        self.button = QPushButton("&Aktualisieren", self)
        self.button.clicked.connect(lambda: self.push_button())
        self.button_forecast = QPushButton("&4-Tage-Vorhersage", self)
        self.button_forecast.clicked.connect(
            lambda: self.push_button_forecast())
        self.Drop.setCurrentIndex(self.Drop.findText(preset['Station']))
        self.Drop.currentIndexChanged.connect(lambda: self.push_button())

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint)
        self.setWindowIcon(QIcon('cloud.png'))
        self.grid = QGridLayout()
        self.grid.addWidget(self.Drop, 0, 0)
        self.grid.addWidget(self.label, 1, 0)
        self.grid.addWidget(self.button_forecast, 2, 0)
        self.grid.addWidget(self.button, 3, 0)
        self.set_image()
        self.setFixedSize(self.pixmap.width()+100, self.pixmap.height()+110)
        self.setLayout(self.grid)
        self.show()

    def set_image(self):
        try:
            self.pixmap = QPixmap()
            self.url_data = urlopen('http://wetterstationen.meteomedia.de/messnetz/wettergrafik/' +
                                    self.Stationen[0][self.Drop.currentText()] + '.png').read()
            self.pixmap.loadFromData(self.url_data)
        except Exception as e:
            print(e)
            self.pixmap = QPixmap('Lade_Error.png')
        self.label.setPixmap(self.pixmap)

    def push_button(self):
        self.set_image()
        self.hide()
        self.show()

    def push_button_forecast(self):
        try:
            url_data = urlopen('http://wetterstationen.meteomedia.de/messnetz/vorhersagegrafik/' + self.Stationen[0][self.Drop.currentText()] + '.png').read()
            self.Forecast_window = App_Forecast(url_data)
            self.Forecast_window.show()
        except Exception as e:
            self.Error_message_URL_Forecast()

    def closeEvent(self, event):
        if self.Stationen[1]:
            preset['Stationsliste'] = self.Stationen[0]
        preset['Station'] = self.Drop.currentText()
        with open('preset.json', 'w') as file:
            json.dump(preset, file)
        event.accept()

    def Error_message_URL_Forecast(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(f"Vorhersage kann nicht abgerufen werden. Bitte versuche es später nocheinmal.")
        msg.setWindowTitle("URL nicht erreichbar")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()


class App_Forecast(QWidget):
    def __init__(self, url_data):
        super().__init__()
        self.url_data = url_data
        self.title = 'Wettervorhersage 4-Tage-Prognose'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('cloud.png'))
        self.label = QLabel(self)
        self.set_image()
        self.setFixedSize(self.pixmap.width(), self.pixmap.height())
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint)
        self.show()

    def set_image(self):
        self.pixmap = QPixmap()
        # self.url_data = urlopen('1http://wetterstationen.meteomedia.de/messnetz/vorhersagegrafik/' +
        #                         self.Stationen[0][self.Drop] + '.png').read()
        self.pixmap.loadFromData(self.url_data)
        self.label.setPixmap(self.pixmap)


if __name__ == '__main__':
    try:
        with open('preset.json', 'r') as json_file:
            preset = json.load(json_file)
            # preset = json.loads(preset)
    except Exception as e:
        print('json laden ging schief:\n', e)
        preset = """{"Station" : "Chemnitz (420m)","Stationsliste" : {"Chemnitz (420m)":"105770","Berlin-Tegel (37m)":"103820"} }"""
        preset = json.loads(preset)

    app = QApplication(sys.argv)
    ex = App(read_weather_stations(), preset)

    sys.exit(app.exec_())

    # read_weather_stations()
