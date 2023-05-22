import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap

from PyQt5 import uic
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        uic.loadUi("solarinterface.ui", self)

        icon = QIcon()

        icon.addPixmap(QPixmap('pic/x.png'))
        self.closeNotificationBtn.setIcon(icon)
        self.closeNotificationBtn.setIconSize(QSize(32, 32))

        icon.addPixmap(QPixmap('pic/menu.png'))
        self.MenuButton.setIcon(icon)
        self.MenuButton.setIconSize(QSize(32, 32))

        icon.addPixmap(QPixmap('pic/flares.png'))
        self.FlaresButton.setIcon(icon)
        self.FlaresButton.setIconSize(QSize(32, 32))

        icon.addPixmap(QPixmap('pic/sun.png'))
        self.SolarButton.setIcon(icon)
        self.SolarButton.setIconSize(QSize(32, 32))

        icon.addPixmap(QPixmap('pic/weather.png'))
        self.WeatherButton.setIcon(icon)
        self.WeatherButton.setIconSize(QSize(32, 32))

        icon.addPixmap(QPixmap('pic/help.png'))
        self.helpBtn.setIcon(icon)
        self.helpBtn.setIconSize(QSize(32, 32))

        icon.addPixmap(QPixmap('pic/info.png'))
        self.infoBtn.setIcon(icon)
        self.infoBtn.setIconSize(QSize(32, 32))

        icon.addPixmap(QPixmap('pic/settings.png'))
        self.settingsBtn.setIcon(icon)
        self.settingsBtn.setIconSize(QSize(32, 32))

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
