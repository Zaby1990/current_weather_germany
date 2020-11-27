import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QPushButton, QFrame, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from urllib.request import urlopen


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Chemnitz'
        self.left = 1700
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
        self.setFixedSize(self.pixmap.width()+23, self.pixmap.height()+50)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint)
        self.button = QPushButton("&Aktualisieren", self)
        self.button.clicked.connect(lambda: self.push_button())

        self.grid = QGridLayout()
        self.grid.addWidget(self.label,0,0)
        self.grid.addWidget(self.button,1,0)
        self.setLayout(self.grid)
        self.show()

    def set_image(self):
        try:
            self.pixmap = QPixmap()
            self.url_data = urlopen(
                'http://wetterstationen.meteomedia.de/messnetz/wettergrafik/105770.png').read()
            self.pixmap.loadFromData(self.url_data)
        except:
            self.pixmap = QPixmap('Lade_Error.png')
        self.label.setPixmap(self.pixmap)

    def push_button(self):
        self.set_image()
        self.hide()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    sys.exit(app.exec_())
