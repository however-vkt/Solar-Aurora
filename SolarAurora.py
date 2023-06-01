import asyncio
from aiohttp import ClientConnectorError
import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import *

import Client

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        uic.loadUi("solarinterface.ui", self)

        self.city = ''
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

        self.btnWeatherCurrent.clicked.connect(lambda: self.get_location('current'))
        self.btnWeatherForecast.clicked.connect(lambda: self.get_location('forecast'))

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
    def get_location(self, type):
        self.city = self.lineEdit_location.text()
        if (type == 'current'):
            self.weatherPages.setCurrentWidget(self.page_current)
            cur = Client.WeatherInfo()
        if (type =='forecast'):
            self.weatherPages.setCurrentWidget(self.page_forecast)
        print(self.city)


async def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    s2h = Client.SolarInfo()
    s1d = Client.SolarInfo()
    s3d = Client.SolarInfo()

    weather = Client.WeatherInfo()

    f6h = Client.SolarFlares()
    f1d = Client.SolarFlares()
    f3d = Client.SolarFlares()

    result_s2h = await s2h.get_solarinfo_2h()
    result_s1d = await s1d.get_solarinfo_1d()
    result_s3d = await s3d.get_solarinfo_3d()

    if ((Exception == result_s2h) or (Exception == result_s1d) or (Exception == result_s3d)):
        print(f'HTTP error occured: Cannot connect to host')
        window.frame_7.setStyleSheet("background-color:red;")
    else:
        window.frame_7.setStyleSheet("background-color:#34C924;")
        print(result_s2h)
        print(result_s1d)
        print(result_s3d)
    #
    #while(not window.lineEdit_location.textChanged.connect()):
    #    if (window.city == ''):
    #        window.label_weathercurrent.setText('Error:\nCity not specified or another error occurred')
    #        window.label_weatherforecast.setText('Error:\nCity not specified or another error occurred')
    #        result_w = 0
    #    else:
    #        result_w = await weather.get_weather(window.city)
    #
    #if (Exception == result_w):
    #    print(f'HTTP error occured: Cannot connect to host')
    #    window.frame_7.setStyleSheet("background-color:red;")
    #else:
    #    window.frame_7.setStyleSheet("background-color:#34C924;")
    #    print(result_w)
    ##result_f6h = await f6h.get_solarflares_6h()
    #result_f1d = await f1d.get_solarflares_1d()
    #result_f3d = await f3d.get_solarflares_3d()

    sys.exit(app.exec_())


if __name__ == "__main__":
    asyncio.run(main())
