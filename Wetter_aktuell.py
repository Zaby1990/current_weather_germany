import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QPushButton, QFrame, QGridLayout, QComboBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from urllib.request import urlopen
import re

Station_Number = 105770


def read_weather_stations():
    try:
        c = urlopen('http://wetterstationen.meteomedia.de/', timeout=1)
        a = str(c.read(), 'utf-8')
        # print(a)
        print('url erfolgreich gelesen')
        with open('html_old.txt', 'w') as i:
            i.write(a)
        print('url erfolgreich gespeichert')
    except Exception as e:
        print(e)
        with open('html_old.txt', 'r') as i:
            a = i.read()
        print('alte url erfolgreich eingelesen')

    a1 = a.split('\n')
    # [print(i) for i in a1]
    ai1 = a1.index('<map name="Karte">')+1
    ai2 = a1.index('</map>')
    Stationen=dict()
    for i in a1[ai1:ai2]:
        stat_no = re.search('[0-9]{6}',i).group()
        stat_name = i[re.search('title="',i).span()[1]:re.search('">',i).span()[0]].replace('&Auml;','Ä').replace('&Ouml;','Ö').replace('&Uuml;','Ü').replace('&auml;','ä').replace('&ouml;','ö').replace('&uuml;','ü').replace('&szlig;','ß')
        Stationen[stat_name]=stat_no
    return Stationen 

class App(QWidget):

    # url_current = 'http://wetterstationen.meteomedia.de/messnetz/wettergrafik/' + \
    #     str(Station_Number) + '.png'

    def __init__(self):
        super().__init__()
        self.title = 'Chemnitz'
        self.left = 1700
        self.top = 100
        self.width = 640
        self.height = 480
        self.Stationen = read_weather_stations()
        self.initUI()


    def initUI(self):
        print(self.url_current)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint)
        self.setWindowIcon(QIcon('cloud.png'))

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.set_image()
        self.setFixedSize(self.pixmap.width()+100, self.pixmap.height()+110)
        self.button = QPushButton("&Aktualisieren", self)
        self.button.clicked.connect(lambda: self.push_button())
        self.button_V = QPushButton("&4-Tage-Prognose", self)
        self.button_V.clicked.connect(lambda: self.push_button_V())
        # DropDownMenue
        self.Drop = QComboBox(self)
        for i in self.Stationen.keys():
            self.Drop.addItem(i)


        self.grid = QGridLayout()
        self.grid.addWidget(self.Drop, 0, 0)
        self.grid.addWidget(self.label, 1, 0)
        self.grid.addWidget(self.button_V, 2, 0)
        self.grid.addWidget(self.button, 3, 0)
        self.setLayout(self.grid)
        self.show()

    def set_image(self):
        try:
            self.pixmap = QPixmap()
            self.url_data = urlopen(self.url_current).read()
            self.pixmap.loadFromData(self.url_data)
        except Exception as e:
            print(e)
            self.pixmap = QPixmap('Lade_Error.png')
        self.label.setPixmap(self.pixmap)

    def push_button(self):
        self.set_image()
        self.hide()
        self.show()

    def push_button_V(self):
        self.prognose_window = App_Prognose()
        self.prognose_window.show()


class App_Prognose(QWidget):
    url_prognose = 'http://wetterstationen.meteomedia.de/messnetz/vorhersagegrafik/' + \
        self.Stationen[self.Drop.currentText()] + '.png'

    def __init__(self):
        super().__init__()
        self.title = 'Chemnitz'
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
        try:
            self.pixmap = QPixmap()
            self.url_data = urlopen(self.url_prognose).read()
            self.pixmap.loadFromData(self.url_data)
        except Exception as e:
            print(e)
            self.pixmap = QPixmap('Lade_Error.png')
        self.label.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    sys.exit(app.exec_())

    # read_weather_stations()
