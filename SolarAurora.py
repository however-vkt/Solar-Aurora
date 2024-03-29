import time

import requests

from PyQt5.QtCore import QSize, QTimer
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
            "A notification pops up for aurora monitoring when 5 conditions match:\n\n\n" +
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

        # Кнопка - Notification
        icon = QIcon()
        icon.addPixmap(QPixmap('pic/bell.png'))
        self.btnNotification.setIcon(icon)
        self.btnNotification.setIconSize(QSize(32, 32))
        self.btnNotification.clicked.connect(lambda: self.check_situation())

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

        self.btnSolar2h.clicked.connect(lambda: self.get_graphics_solarinfo('2h'))
        self.btnSolar1d.clicked.connect(lambda: self.get_graphics_solarinfo('1d'))
        self.btnSolar3d.clicked.connect(lambda: self.get_graphics_solarinfo('3d'))

        self.btnFlares6h.clicked.connect(lambda: self.get_graphics_flares('6h'))
        self.btnFlares1d.clicked.connect(lambda: self.get_graphics_flares('1d'))
        self.btnFlares3d.clicked.connect(lambda: self.get_graphics_flares('3d'))

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

        self.GraphWidget_flares_6h.setBackground('w')
        self.GraphWidget_flares_6h.setTitle('Kp(Date)')
        self.GraphWidget_flares_6h.setLabel('left', 'Kp')
        self.GraphWidget_flares_6h.setLabel('bottom', 'Date')
        self.GraphWidget_flares_6h.addLine(x=None, y=0, pen='black')

        self.GraphWidget_flares_1d.setBackground('w')
        self.GraphWidget_flares_1d.setTitle('Kp(Date)')
        self.GraphWidget_flares_1d.setLabel('left', 'Kp')
        self.GraphWidget_flares_1d.setLabel('bottom', 'Date')
        self.GraphWidget_flares_1d.addLine(x=None, y=0, pen='black')

        self.GraphWidget_flares_3d.setBackground('w')
        self.GraphWidget_flares_3d.setTitle('Kp(Date)')
        self.GraphWidget_flares_3d.setLabel('left', 'Kp')
        self.GraphWidget_flares_3d.setLabel('bottom', 'Date')
        self.GraphWidget_flares_3d.addLine(x=None, y=0, pen='black')

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
            print()
            x = date_merge["longtime"]
            y = np.array(date_merge["value"], dtype=float)
            self.GraphWidget_bz_2h.plot(x, y,  kind="scatter", pen='black')
            self.GraphWidget_bz_2h.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_bz_2h.getPlotItem().hideAxis('bottom')

            y = np.array(s2h.bt, dtype=float)
            self.GraphWidget_bt_2h.plot(x, y,  kind="scatter", pen='black')
            self.GraphWidget_bt_2h.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_bt_2h.getPlotItem().hideAxis('bottom')

            date_merge = pd.DataFrame({"longtime": s2h.dateUP, "value": s2h.u})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s2h.u, dtype=float)
            self.GraphWidget_u_2h.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_u_2h.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_u_2h.getPlotItem().hideAxis('bottom')

            y = np.array(s2h.p, dtype=float)
            self.GraphWidget_p_2h.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_p_2h.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_p_2h.getPlotItem().hideAxis('bottom')

            date_merge = pd.DataFrame({"longtime": s2h.dateDST, "value": s2h.DST})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s2h.DST, dtype=float)
            self.GraphWidget_DST_2h.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_DST_2h.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_DST_2h.getPlotItem().hideAxis('bottom')

            date_merge = pd.DataFrame({"longtime": s2h.dateKp, "value": s2h.Kp})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s2h.Kp, dtype=float)
            self.GraphWidget_Kp_2h.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_Kp_2h.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_Kp_2h.getPlotItem().hideAxis('bottom')
        if (type == '1d'):
            self.solarPages.setCurrentWidget(self.page_1d)

            s1d = Client.SolarInfo()
            s1d.get_solarinfo_1d()

            date_merge = pd.DataFrame({"longtime": s1d.dateBzBt, "value": s1d.bz})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]

            y = np.array(s1d.bz, dtype=float)
            self.GraphWidget_bz_1d.plot(x, y, pen='black')
            self.GraphWidget_bz_1d.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_bz_1d.getPlotItem().hideAxis('bottom')

            y = np.array(s1d.bt, dtype=float)
            self.GraphWidget_bt_1d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_bt_1d.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_bt_1d.getPlotItem().hideAxis('bottom')

            date_merge = pd.DataFrame({"longtime": s1d.dateUP, "value": s1d.u})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s1d.u, dtype=float)
            self.GraphWidget_u_1d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_u_1d.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_u_1d.getPlotItem().hideAxis('bottom')

            y = np.array(s1d.p, dtype=float)
            self.GraphWidget_p_1d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_p_1d.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_p_1d.getPlotItem().hideAxis('bottom')

            date_merge = pd.DataFrame({"longtime": s1d.dateDST, "value": s1d.DST})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s1d.DST, dtype=float)
            self.GraphWidget_DST_1d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_DST_1d.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_DST_1d.getPlotItem().hideAxis('bottom')

            date_merge = pd.DataFrame({"longtime": s1d.dateKp, "value": s1d.Kp})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s1d.Kp, dtype=float)
            self.GraphWidget_Kp_1d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_Kp_1d.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_Kp_1d.getPlotItem().hideAxis('bottom')
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
            self.GraphWidget_bz_3d.getPlotItem().hideAxis('bottom')

            y = np.array(s3d.bt, dtype=float)
            self.GraphWidget_bt_3d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_bt_3d.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_bt_3d.getPlotItem().hideAxis('bottom')

            date_merge = pd.DataFrame({"longtime": s3d.dateUP, "value": s3d.u})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s3d.u, dtype=float)
            self.GraphWidget_u_3d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_u_3d.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_u_3d.getPlotItem().hideAxis('bottom')

            y = np.array(s3d.p, dtype=float)
            self.GraphWidget_p_3d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_p_3d.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_p_3d.getPlotItem().hideAxis('bottom')

            date_merge = pd.DataFrame({"longtime": s3d.dateDST, "value": s3d.DST})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s3d.DST, dtype=float)
            self.GraphWidget_DST_3d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_DST_3d.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_DST_3d.getPlotItem().hideAxis('bottom')

            date_merge = pd.DataFrame({"longtime": s3d.dateKp, "value": s3d.Kp})
            date_merge["longtime"] = pd.to_datetime(date_merge["longtime"])
            x = date_merge["longtime"]
            y = np.array(s3d.Kp, dtype=float)
            self.GraphWidget_Kp_3d.plot(x, y, kind="scatter", pen='black')
            self.GraphWidget_Kp_3d.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_Kp_3d.getPlotItem().hideAxis('bottom')

    def get_graphics_flares(self, type):
        self.raise_server_status()
        if (type == '6h'):
            self.flaresPages.setCurrentWidget(self.page_flares_6h)

            s6h = Client.SolarFlares()
            s6h.get_solarflares_6h()

            y = np.array(s6h.flux, dtype=float)
            self.GraphWidget_flares_6h.plot(y, kind="scatter", pen='black')
            self.GraphWidget_flares_6h.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_flares_6h.getPlotItem().hideAxis('bottom')
        if (type == '1d'):
            self.flaresPages.setCurrentWidget(self.page_flares_1d)

            s1d = Client.SolarFlares()
            s1d.get_solarflares_1d()

            y = np.array(s1d.flux, dtype=float)
            self.GraphWidget_flares_1d.plot(y, kind="scatter", pen='black')
            self.GraphWidget_flares_1d.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_flares_1d.getPlotItem().hideAxis('bottom')
        if (type == '3d'):
            self.flaresPages.setCurrentWidget(self.page_flares_3d)

            s3d = Client.SolarFlares()
            s3d.get_solarflares_3d()

            y = np.array(s3d.flux, dtype=float)
            self.GraphWidget_flares_3d.plot(y, kind="scatter", pen='black')
            self.GraphWidget_flares_3d.plotItem.setMouseEnabled(x=False, y=False)
            self.GraphWidget_flares_3d.getPlotItem().hideAxis('bottom')

    def check_situation(self):
        self.popupNotificationContainer.show()
        s2h = Client.SolarInfo()
        s2h.get_solarinfo_2h()
        bz = np.array(s2h.bz, dtype=float)
        kp = np.array(s2h.Kp, dtype=float)
        p = np.array(s2h.p, dtype=float)
        u = np.array(s2h.u, dtype=float)
        av = sum(bz)/len(bz)
        print(bz[len(bz)-1])
        print(p[len(p)-1])
        print(u[len(u)-1])
        print(kp[len(kp)-1])
        print(av)
        if ((kp[len(kp)-1] >= 7) and (p[len(p)-1] > 25) and (u[len(u)-1] > 650) and (
                bz[len(bz)-1] <= -15 and av < 0)):
            self.label_13.setText("Very high solar activity")
            self.label_13.setStyleSheet("background-color:red;")
            print('red status')
            return
        if ((kp[len(kp)-1] >= 6) and (p[len(p)-1] > 20) and (u[len(u)-1] > 550) and (
                bz[len(bz)-1] <= -12 and av < 0)):
            self.label_13.setText("High solar activity")
            self.label_13.setStyleSheet("background-color:#FF4500;")
            print('dark orange status')
            return
        if ((kp[len(kp)-1] >= 6) and (p[len(p)-1] > 25) and (u[len(u)-1] > 500) and (
                bz[len(bz)-1] <= -12 and av < 0)):
            self.label_13.setText("Medium solar activity")
            self.label_13.setStyleSheet("background-color:#FF8C00;")
            print('orange status')
            return
        if ((kp[len(kp)-1] >= 5) and (p[len(p)-1] > 20) and (u[len(u)-1] > 500) and (
                bz[len(bz)-1] <= -10 and av < 0)):
            self.label_13.setText("Low solar activity")
            self.label_13.setStyleSheet("background-color:#FFA500;")
            print('yellow status')
            return
        self.label_13.setText("Very low solar activity")
        self.label_13.setStyleSheet("background-color:#9ACD32;")
        print('green status')
        return
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.check_situation()

    sys.exit(app.exec_())