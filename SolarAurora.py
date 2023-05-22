import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

import icons.ico

from PyQt5 import uic
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        uic.loadUi("solarinterface.ui", self)
        self.show()

        # closeNotificationBtn
        #
        # MenuButton
        #
        # FlaresButton
        # SolarButton
        # WeatherButton
        #
        # helpBtn
        # infoBtn
        # settingsBtn

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
