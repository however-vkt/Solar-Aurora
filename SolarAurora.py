import asyncio
import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap

from PyQt5 import uic
from PyQt5.QtWidgets import *
from aiohttp import ClientConnectorError

import Client

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        uic.loadUi("solarinterface.ui", self)

########################################################################################################################
#                       Инициализация основных объектов
########################################################################################################################

        self.s2h = Client.SolarInfo()
        self.s1d = Client.SolarInfo()
        self.s3d = Client.SolarInfo()

        self.city = ''
        self.weather = Client.WeatherInfo()

        self.f6h = Client.SolarFlares()
        self.f1d = Client.SolarFlares()
        self.f3d = Client.SolarFlares()

########################################################################################################################
#                       Инициализация основных кнопок
########################################################################################################################
        # Кнопка - Notification
        icon = QIcon()
        icon.addPixmap(QPixmap('pic/bell.png'))
        self.btnNotification.setIcon(icon)
        self.btnNotification.setIconSize(QSize(32, 32))
        self.btnNotification.clicked.connect(lambda: self.popupNotificationContainer.show())

        # Кнопка - Close Notification
        icon.addPixmap(QPixmap('pic/x.png'))
        self.closeNotificationBtn.setIcon(icon)
        self.closeNotificationBtn.setIconSize(QSize(32, 32))
        self.closeNotificationBtn.clicked.connect(lambda: self.popupNotificationContainer.close())

        # Кнопка - Menu
        icon.addPixmap(QPixmap('pic/menu.png'))
        self.MenuButton.setIcon(icon)
        self.MenuButton.setIconSize(QSize(32, 32))
        self.changed = False
        self.MenuButton.clicked.connect(lambda: self.expand_or_collapse(self.changed))

        # Кнопка - Sun
        icon.addPixmap(QPixmap('pic/sun.png'))
        self.SolarButton.setIcon(icon)
        self.SolarButton.setIconSize(QSize(32, 32))
        self.SolarButton.clicked.connect(lambda: self.mainPages.setCurrentWidget(self.page_solar))

        # Кнопка - Weather
        icon.addPixmap(QPixmap('pic/weather.png'))
        self.WeatherButton.setIcon(icon)
        self.WeatherButton.setIconSize(QSize(32, 32))
        self.WeatherButton.clicked.connect(lambda: self.mainPages.setCurrentWidget(self.page_weather))

        # Кнопка - Flares
        icon.addPixmap(QPixmap('pic/flares.png'))
        self.FlaresButton.setIcon(icon)
        self.FlaresButton.setIconSize(QSize(32, 32))
        self.FlaresButton.clicked.connect(lambda: self.mainPages.setCurrentWidget(self.page_flares))

        icon.addPixmap(QPixmap('pic/help.png'))
        self.helpBtn.setIcon(icon)
        self.helpBtn.setIconSize(QSize(32, 32))
        self.helpBtn.clicked.connect(lambda: self.mainPages.setCurrentWidget(self.page_help))

        icon.addPixmap(QPixmap('pic/info.png'))
        self.infoBtn.setIcon(icon)
        self.infoBtn.setIconSize(QSize(32, 32))
        self.infoBtn.clicked.connect(lambda: self.mainPages.setCurrentWidget(self.page_info))

        icon.addPixmap(QPixmap('pic/settings.png'))
        self.settingsBtn.setIcon(icon)
        self.settingsBtn.setIconSize(QSize(32, 32))
        self.settingsBtn.clicked.connect(lambda: self.mainPages.setCurrentWidget(self.page_settings))

########################################################################################################################
#                       Инициализация основных событий
########################################################################################################################

        self.btnSolar2h.clicked.connect(lambda: self.solarPages.setCurrentWidget(self.page_2h))
        self.btnSolar1d.clicked.connect(lambda: self.solarPages.setCurrentWidget(self.page_1d))
        self.btnSolar3d.clicked.connect(lambda: self.solarPages.setCurrentWidget(self.page_3d))
        #
        #self.btnWeatherCurrent.clicked.connect()
        #self.btnWeatherForecast.clicked.connect()
        #
        #self.btnFlares6h.clicked.connect()
        #self.btnFlares1d.clicked.connect()
        #self.btnFlares3d.clicked.connect()

        self.GraphWidget_bz_2h.setBackground('w')
        self.GraphWidget_bt_2h.setBackground('w')
        self.GraphWidget_u_2h.setBackground('w')
        self.GraphWidget_p_2h.setBackground('w')
        self.GraphWidget_DST_2h.setBackground('w')
        self.GraphWidget_Kp_2h.setBackground('w')

        self.GraphWidget_bz_1d.setBackground('w')
        self.GraphWidget_bt_1d.setBackground('w')
        self.GraphWidget_u_1d.setBackground('w')
        self.GraphWidget_p_1d.setBackground('w')
        self.GraphWidget_DST_1d.setBackground('w')
        self.GraphWidget_Kp_1d.setBackground('w')

        self.GraphWidget_bz_3d.setBackground('w')
        self.GraphWidget_bt_3d.setBackground('w')
        self.GraphWidget_u_3d.setBackground('w')
        self.GraphWidget_p_3d.setBackground('w')
        self.GraphWidget_DST_3d.setBackground('w')
        self.GraphWidget_Kp_3d.setBackground('w')

        self.show()

    def expand_menu(self):
        self.leftMenuContainer.setFixedWidth(350)
    def collapse_menu(self):
        self.leftMenuContainer.setFixedWidth(60)
    def expand_or_collapse(self, changed):
        if (not changed):
            self.collapse_menu()
            self.changed = True
        else:
            self.expand_menu()
            self.changed = False

async def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    s2h = Client.SolarInfo()
    result = await s2h.get_solarinfo_2h()
    if (ClientConnectorError):
        print(result)
    else:
        print(result.get('0'))
        print(result.get('1'))

    sys.exit(app.exec_())

if __name__ == "__main__":
    asyncio.run(main())
