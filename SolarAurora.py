import requests
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

        self.label_info.setText("Bz indicates the orientation of the IMF.\n\n" +
            "Bt - parameter that showing the interplanetary magnetic field ( IMF ).\n\n" +
            "u - cosmic wind speed.\n\n" +
            "p - solar flux density.\n\n" +
            "DST - temporary recession index.\n\n" +
            "Kp-index is the global geomagnetic activity index that is based on 3-hour measurements" +
            "from ground-based magnetometers around the world.\n\n\n" +
            "A notification pops up for aurora monitoring when 3 conditions match:\n\n\n" +
            "Kp >= 5 ( non-priority )\n\n" +
            "p > 20\n\n" +
            "u > 500\n\n" +
            "bz <= -10\n\n" +
            "average bz for the last hour < 0\n\n")

        self.label_settings.setText("There will be screen size settings\n\nLight/Dark theme feature\n\n"+
                                   "Notification volume control\n\nNotification style control")
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

        self.raise_server_status()

        self.show()

    def raise_server_status(self):
        url = f'http://localhost:8080/solarinfo?tag=s2h'
        try:
            print("checking status")
            req = requests.get(url)
            req.raise_for_status()
            self.frame_7.setStyleSheet("background-color:#34C924;")
        except Exception as ex:
            self.frame_7.setStyleSheet("background-color:red;")
            print(ex)

    def expand_menu(self):
        self.leftMenuContainer.setFixedWidth(350)
    def collapse_menu(self):
        self.leftMenuContainer.setFixedWidth(60)
    def expand_or_collapse(self, changed):
        self.raise_server_status()
        if (not changed):
            self.collapse_menu()
            self.changed = True
        else:
            self.expand_menu()
            self.changed = False
    def get_location(self, type):
        self.raise_server_status()
        self.city = self.lineEdit_location.text()
        if (type == 'current'):
            self.weatherPages.setCurrentWidget(self.page_current)
            cur = Client.WeatherInfo()
            cur.get_weather(self.city)
            self.label_weathercurrent.setText(cur.get_info_cur())
        if (type =='forecast'):
            self.weatherPages.setCurrentWidget(self.page_forecast)
            forecast = Client.WeatherInfo()
            forecast.get_weather(self.city)
            self.label_weatherforecast.setText(forecast.get_info_forecast())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
