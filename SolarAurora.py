import requests
import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import *

import Client

import pandas as pd
import numpy as np

from matplotlib import *

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

        self.label_help.setText("The application was created to monitoring solar activity and forecasting auroras\n\n" +
                                "There is email to receive feedback:\n\n\n" +
                                "however.viktor@gmail.com")
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

        self.btnSolar2h.clicked.connect(lambda: self.get_graphics_solarinfo('2h'))
        self.btnSolar1d.clicked.connect(lambda: self.get_graphics_solarinfo('1d'))
        self.btnSolar3d.clicked.connect(lambda: self.get_graphics_solarinfo('3d'))

        #
        #self.btnWeatherCurrent.clicked.connect()
        #self.btnWeatherForecast.clicked.connect()
        #
        #self.btnFlares6h.clicked.connect()
        #self.btnFlares1d.clicked.connect()
        #self.btnFlares3d.clicked.connect()

        self.GraphWidget_bz_2h.setBackground('w')
        self.GraphWidget_bz_2h.setTitle('Bz(Date)')
        self.GraphWidget_bz_2h.setLabel('left', 'Bz')
        self.GraphWidget_bz_2h.setLabel('bottom', 'Date')
        self.GraphWidget_bz_2h.addLine(x=None, y=0, pen='black')
        self.GraphWidget_bz_2h.addLine(x=None, y=10, pen='red')
        self.GraphWidget_bz_2h.addLine(x=None, y=-10, pen='red')

        self.GraphWidget_bt_2h.setBackground('w')
        self.GraphWidget_bt_2h.setTitle('Bt(Date)')
        self.GraphWidget_bt_2h.setLabel('left', 'Bt')
        self.GraphWidget_bt_2h.setLabel('bottom', 'Date')
        self.GraphWidget_bt_2h.addLine(x=None, y=0, pen='black')

        self.GraphWidget_u_2h.setBackground('w')
        self.GraphWidget_u_2h.setTitle('u(Date)')
        self.GraphWidget_u_2h.setLabel('left', 'u')
        self.GraphWidget_u_2h.setLabel('bottom', 'Date')
        self.GraphWidget_u_2h.addLine(x=None, y=0, pen='black')

        self.GraphWidget_p_2h.setBackground('w')
        self.GraphWidget_p_2h.setTitle('p(Date)')
        self.GraphWidget_p_2h.setLabel('left', 'p')
        self.GraphWidget_p_2h.setLabel('bottom', 'Date')
        self.GraphWidget_p_2h.addLine(x=None, y=0, pen='black')

        self.GraphWidget_DST_2h.setBackground('w')
        self.GraphWidget_DST_2h.setTitle('DST(Date)')
        self.GraphWidget_DST_2h.setLabel('left', 'DST')
        self.GraphWidget_DST_2h.setLabel('bottom', 'Date')
        self.GraphWidget_DST_2h.addLine(x=None, y=0, pen='black')

        self.GraphWidget_Kp_2h.setBackground('w')
        self.GraphWidget_Kp_2h.setTitle('Kp(Date)')
        self.GraphWidget_Kp_2h.setLabel('left', 'Kp')
        self.GraphWidget_Kp_2h.setLabel('bottom', 'Date')
        self.GraphWidget_Kp_2h.addLine(x=None, y=0, pen='black')

        self.GraphWidget_bz_1d.setBackground('w')
        self.GraphWidget_bz_1d.setTitle('Bz(Date)')
        self.GraphWidget_bz_1d.setLabel('left', 'Bz')
        self.GraphWidget_bz_1d.setLabel('bottom', 'Date')
        self.GraphWidget_bz_1d.addLine(x=None, y=0, pen='black')
        self.GraphWidget_bz_1d.addLine(x=None, y=10, pen='red')
        self.GraphWidget_bz_1d.addLine(x=None, y=-10, pen='red')

        self.GraphWidget_bt_1d.setBackground('w')
        self.GraphWidget_bt_1d.setTitle('Bt(Date)')
        self.GraphWidget_bt_1d.setLabel('left', 'Bt')
        self.GraphWidget_bt_1d.setLabel('bottom', 'Date')
        self.GraphWidget_bt_1d.addLine(x=None, y=0, pen='black')

        self.GraphWidget_u_1d.setBackground('w')
        self.GraphWidget_u_1d.setTitle('u(Date)')
        self.GraphWidget_u_1d.setLabel('left', 'u')
        self.GraphWidget_u_1d.setLabel('bottom', 'Date')
        self.GraphWidget_u_1d.addLine(x=None, y=0, pen='black')

        self.GraphWidget_p_1d.setBackground('w')
        self.GraphWidget_p_1d.setTitle('p(Date)')
        self.GraphWidget_p_1d.setLabel('left', 'p')
        self.GraphWidget_p_1d.setLabel('bottom', 'Date')
        self.GraphWidget_p_1d.addLine(x=None, y=0, pen='black')

        self.GraphWidget_DST_1d.setBackground('w')
        self.GraphWidget_DST_1d.setTitle('DST(Date)')
        self.GraphWidget_DST_1d.setLabel('left', 'DST')
        self.GraphWidget_DST_1d.setLabel('bottom', 'Date')
        self.GraphWidget_DST_1d.addLine(x=None, y=0, pen='black')

        self.GraphWidget_Kp_1d.setBackground('w')
        self.GraphWidget_Kp_1d.setTitle('Kp(Date)')
        self.GraphWidget_Kp_1d.setLabel('left', 'Kp')
        self.GraphWidget_Kp_1d.setLabel('bottom', 'Date')
        self.GraphWidget_Kp_1d.addLine(x=None, y=0, pen='black')

        self.GraphWidget_bz_3d.setBackground('w')
        self.GraphWidget_bz_3d.setTitle('Bz(Date)')
        self.GraphWidget_bz_3d.setLabel('left', 'Bz')
        self.GraphWidget_bz_3d.setLabel('bottom', 'Date')
        self.GraphWidget_bz_3d.addLine(x=None, y=0, pen='black')
        self.GraphWidget_bz_3d.addLine(x=None, y=10, pen='red')
        self.GraphWidget_bz_3d.addLine(x=None, y=-10, pen='red')

        self.GraphWidget_bt_3d.setBackground('w')
        self.GraphWidget_bt_3d.setTitle('Bt(Date)')
        self.GraphWidget_bt_3d.setLabel('left', 'Bt')
        self.GraphWidget_bt_3d.setLabel('bottom', 'Date')
        self.GraphWidget_bt_3d.addLine(x=None, y=0, pen='black')

        self.GraphWidget_u_3d.setBackground('w')
        self.GraphWidget_u_3d.setTitle('u(Date)')
        self.GraphWidget_u_3d.setLabel('left', 'u')
        self.GraphWidget_u_3d.setLabel('bottom', 'Date')
        self.GraphWidget_u_3d.addLine(x=None, y=0, pen='black')

        self.GraphWidget_p_3d.setBackground('w')
        self.GraphWidget_p_3d.setTitle('p(Date)')
        self.GraphWidget_p_3d.setLabel('left', 'p')
        self.GraphWidget_p_3d.setLabel('bottom', 'Date')
        self.GraphWidget_p_3d.addLine(x=None, y=0, pen='black')

        self.GraphWidget_DST_3d.setBackground('w')
        self.GraphWidget_DST_3d.setTitle('DST(Date)')
        self.GraphWidget_DST_3d.setLabel('left', 'DST')
        self.GraphWidget_DST_3d.setLabel('bottom', 'Date')
        self.GraphWidget_DST_3d.addLine(x=None, y=0, pen='black')

        self.GraphWidget_Kp_3d.setBackground('w')
        self.GraphWidget_Kp_3d.setTitle('Kp(Date)')
        self.GraphWidget_Kp_3d.setLabel('left', 'Kp')
        self.GraphWidget_Kp_3d.setLabel('bottom', 'Date')
        self.GraphWidget_Kp_3d.addLine(x=None, y=0, pen='black')

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
    def get_graphics_solarinfo(self, type):
        self.raise_server_status()
        if (type == '2h'):
            self.solarPages.setCurrentWidget(self.page_2h)

            s2h = Client.SolarInfo()
            s2h.get_solarinfo_2h()

            date_merge = pd.DataFrame({"longtime": s2h.dateBzBt, "value": s2h.bz})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(date_merge["value"], dtype=float)
            self.GraphWidget_bz_2h.plot(y,  kind="scatter", pen='black', axisItems={'bottom': s2h.dateBzBt})
            self.GraphWidget_bz_2h.plotItem.setMouseEnabled(x=False, y=False)

            y = np.array(s2h.bt, dtype=float)
            self.GraphWidget_bt_2h.plot(x, y,  kind="scatter", pen='black')
            self.GraphWidget_bt_2h.plotItem.setMouseEnabled(x=False, y=False)

            date_merge = pd.DataFrame({"longtime": s2h.dateUP, "value": s2h.u})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s2h.u, dtype=float)
            self.GraphWidget_u_2h.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_u_2h.plotItem.setMouseEnabled(x=False, y=False)

            y = np.array(s2h.p, dtype=float)
            self.GraphWidget_p_2h.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_p_2h.plotItem.setMouseEnabled(x=False, y=False)

            date_merge = pd.DataFrame({"longtime": s2h.dateDST, "value": s2h.DST})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s2h.DST, dtype=float)
            self.GraphWidget_DST_2h.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_DST_2h.plotItem.setMouseEnabled(x=False, y=False)

            date_merge = pd.DataFrame({"longtime": s2h.dateKp, "value": s2h.Kp})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s2h.Kp, dtype=float)
            self.GraphWidget_Kp_2h.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_Kp_2h.plotItem.setMouseEnabled(x=False, y=False)
        if (type == '1d'):
            self.solarPages.setCurrentWidget(self.page_1d)

            s1d = Client.SolarInfo()
            s1d.get_solarinfo_1d()

            date_merge = pd.DataFrame({"longtime": s1d.dateBzBt, "value": s1d.bz})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(date_merge["value"], dtype=float)
            self.GraphWidget_bz_1d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_bz_1d.plotItem.setMouseEnabled(x=False, y=False)

            y = np.array(s1d.bt, dtype=float)
            self.GraphWidget_bt_1d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_bt_1d.plotItem.setMouseEnabled(x=False, y=False)

            date_merge = pd.DataFrame({"longtime": s1d.dateUP, "value": s1d.u})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s1d.u, dtype=float)
            self.GraphWidget_u_1d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_u_1d.plotItem.setMouseEnabled(x=False, y=False)

            y = np.array(s1d.p, dtype=float)
            self.GraphWidget_p_1d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_p_1d.plotItem.setMouseEnabled(x=False, y=False)

            date_merge = pd.DataFrame({"longtime": s1d.dateDST, "value": s1d.DST})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s1d.DST, dtype=float)
            self.GraphWidget_DST_1d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_DST_1d.plotItem.setMouseEnabled(x=False, y=False)

            date_merge = pd.DataFrame({"longtime": s1d.dateKp, "value": s1d.Kp})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s1d.Kp, dtype=float)
            self.GraphWidget_Kp_1d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_Kp_1d.plotItem.setMouseEnabled(x=False, y=False)
        if (type == '3d'):
            self.solarPages.setCurrentWidget(self.page_3d)

            s3d = Client.SolarInfo()
            s3d.get_solarinfo_3d()

            date_merge = pd.DataFrame({"longtime": s3d.dateBzBt, "value": s3d.bz})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(date_merge["value"], dtype=float)
            self.GraphWidget_bz_3d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_bz_3d.plotItem.setMouseEnabled(x=False, y=False)

            y = np.array(s3d.bt, dtype=float)
            self.GraphWidget_bt_3d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_bt_3d.plotItem.setMouseEnabled(x=False, y=False)

            date_merge = pd.DataFrame({"longtime": s3d.dateUP, "value": s3d.u})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s3d.u, dtype=float)
            self.GraphWidget_u_3d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_u_3d.plotItem.setMouseEnabled(x=False, y=False)

            y = np.array(s3d.p, dtype=float)
            self.GraphWidget_p_3d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_p_3d.plotItem.setMouseEnabled(x=False, y=False)

            date_merge = pd.DataFrame({"longtime": s3d.dateDST, "value": s3d.DST})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s3d.DST, dtype=float)
            self.GraphWidget_DST_3d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_DST_3d.plotItem.setMouseEnabled(x=False, y=False)

            date_merge = pd.DataFrame({"longtime": s3d.dateKp, "value": s3d.Kp})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s3d.Kp, dtype=float)
            self.GraphWidget_Kp_3d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_Kp_3d.plotItem.setMouseEnabled(x=False, y=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
