import requests
from requests import HTTPError


####################################################################################################################
#   Класс для элемента "Солнце"
####################################################################################################################
class SolarInfo:
    def __init__(self):
        self.status = ""

        self.dateBzBt = list()  # Дата со спутника (для bz, bt)
        self.dateUP = list()  # Дата со спутника (для u, p)
        self.dateDST = list()  # Дата для DST
        self.dateKp = list()  # Дата для Kp

        self.bz = list()  # Bz-компонента     [nT]
        self.bt = list()  # Межпланетное магнитное поле (IMF) [nT]
        self.u = list()  # Скорость солнечного ветра [км/с]
        self.p = list()  # Плотность потока  [p/см3]
        self.DST = list()  # Индекс временного спада   [nT]
        self.Kp = list()  # Kp-индекс
        self.KpType = list()  # Тип Kp-индекса (observed, estimated, predicted)

    def get_solarinfo_2h(self):
        # запрашиваем данные у NOAA
        url = 'http://localhost:8080/solarinfo?tag=s2h'

        try:
            req = requests.get(url)
            # Если ответ успешен, то исключения задействованы не будут
            req.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')
        except Exception as err:
            print(f'Other error occured: {err}')
        else:
            print('Success!\n')
            req = requests.get(url)
            info = req.json()

            self.dateBzBt = info.get('0')
            self.bz = info.get('1')
            self.bt = info.get('2')
            self.u = info.get('3')
            self.p = info.get('4')
            self.dateDST = info.get('5')
            self.DST = info.get('6')
            self.dateKp = info.get('7')
            self.Kp = info.get('8')
            self.KpType = info.get('9')

            return info
    def get_solarinfo_1d(self):
        # запрашиваем данные у NOAA
        url = 'http://localhost:8080/solarinfo?tag=s1d'

        try:
            req = requests.get(url)
            # Если ответ успешен, то исключения задействованы не будут
            req.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')
        except Exception as err:
            print(f'Other error occured: {err}')
        else:
            print('Success!\n')
            req = requests.get(url)
            info = req.json()

            self.dateBzBt = info.get('0')
            self.bz = info.get('1')
            self.bt = info.get('2')
            self.u = info.get('3')
            self.p = info.get('4')
            self.dateDST = info.get('5')
            self.DST = info.get('6')
            self.dateKp = info.get('7')
            self.Kp = info.get('8')
            self.KpType = info.get('9')

            return info
    def get_solarinfo_3d(self):
        # запрашиваем данные у NOAA
        url = 'http://localhost:8080/solarinfo?tag=s3d'

        try:
            req = requests.get(url)
            # Если ответ успешен, то исключения задействованы не будут
            req.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')
        except Exception as err:
            print(f'Other error occured: {err}')
        else:
            print('Success!\n')
            req = requests.get(url)
            info = req.json()

            self.dateBzBt = info.get('0')
            self.bz = info.get('1')
            self.bt = info.get('2')
            self.u = info.get('3')
            self.p = info.get('4')
            self.dateDST = info.get('5')
            self.DST = info.get('6')
            self.dateKp = info.get('7')
            self.Kp = info.get('8')
            self.KpType = info.get('9')

            return info

    def get_info(self):
        s = str(self.dateBzBt) + "\n" + str(self.bz) + "\n" + str(self.bt) + "\n" + str(self.u) + "\n" + str(self.p) + "\n" + str(self.dateDST) + "\n" + str(self.DST) + "\n" + str(self.dateKp) + "\n" + str(self.Kp) + "\n" + str(self.KpType) + "\n\n"
        return s

    def check_situation(self):


        return self.status
####################################################################################################################
#   Класс для элемента "Погода"
####################################################################################################################
#
#                                           ЗАПИСАТЬ ДАННЫЕ!!!!!
class WeatherInfo:
    def __init__(self):
        # Данные собираются с WeatherAPI.com
        self.weather = ""
        self.location = dict()
        self.current = dict()
        self.forecast = dict()

    def get_weather(self, city):
        url = f'http://localhost:8080/weather'
        params = {'city': city}
        try:
            req = requests.get(url, params=params)
            # Если ответ успешен, то исключения задействованы не будут
            req.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')
        except Exception as err:
            print(f'Other error occured: {err}')
        else:
            print('Success!\n')
            req = requests.get(url, params=params)
            info = req.json()

            self.location = info.get('0')
            self.current = info['1']
            self.forecast = info['2']['forecastday'][0]['day']
            self.weather = info['2']['forecastday'][0]['day']['condition']['text']

            info = {'location': self.location, 'current': self.current, 'forecast': self.forecast}
            return info

    def get_info_cur(self):
        s = "Name: " + str(self.location.get('name')) + "\n\n" + "Region: " + str(self.location.get('region'))
        s += "\n\n" + "Country: " + str(self.location.get('country')) + "\n\n" + "Local time: " + str(self.location.get('localtime'))
        s += "\n\n\n" + "Temp C: " + str(self.current.get('temp_c')) + "\n\n" + "Feels like: "
        s += str(self.current.get('feelslike_c')) + "\n\n" + "Humidity: " + str(self.current.get('humidity'))
        s += "\n\n" + "Cloud: " + str(self.current.get('cloud')) + "\n\n" + "Wind: " + str(self.current.get('wind_kph'))
        return s

    def get_info_forecast(self):
        s = "Max temperature C: " + str(self.forecast.get('maxtemp_c')) + "\n\n" + "Minimal temperature C: " + str(self.forecast.get('mintemp_c')) + "\n\n"
        s += "Average temperature C: " + str(self.forecast.get('avgtemp_c')) + "\n\n" + "Average humidity: " + str(self.forecast.get('avghumidity')) + "\n\n"
        s += "Daily chance of rain: " + str(self.forecast.get('daily_chance_of_rain')) + "\n\n" + "Weather: " + str(self.weather)
        s += "\n\n\n"
        return s

####################################################################################################################
#   Класс для элемента "Солнечные вспышки"
####################################################################################################################
class SolarFlares:
    def __init__(self):
        self.date = list()      # Дата измерений
        self.flux = list()      # electron flux

    def get_solarflares_6h(self):
        # запрашиваем данные у NOAA
        url = 'http://localhost:8080/flares?tag=s6h'
        try:
            req = requests.get(url)
            # Если ответ успешен, то исключения задействованы не будут
            req.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')
        except Exception as err:
            print(f'Other error occured: {err}')
        else:
            print('Success!\n')
            req = requests.get(url)
            info = req.json()
            self.date = info.get('0')
            self.flux = info.get('1')

            return info
    def get_solarflares_1d(self):
        # запрашиваем данные у NOAA
        url = 'http://localhost:8080/flares?tag=s1d'
        try:
            req = requests.get(url)
            # Если ответ успешен, то исключения задействованы не будут
            req.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')
        except Exception as err:
            print(f'Other error occured: {err}')
        else:
            print('Success!\n')
            req = requests.get(url)
            info = req.json()
            self.date = info.get('0')
            self.flux = info.get('1')

            return info

    def get_solarflares_3d(self):
        # запрашиваем данные у NOAA
        url = 'http://localhost:8080/flares?tag=s3d'
        try:
            req = requests.get(url)
            # Если ответ успешен, то исключения задействованы не будут
            req.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occured: {http_err}')
        except Exception as err:
            print(f'Other error occured: {err}')
        else:
            print('Success!\n')
            req = requests.get(url)
            info = req.json()
            self.date = info.get('0')
            self.flux = info.get('1')

            return info

    def get_info(self):
        s = str(self.date) + "\n" + str(self.flux) + "\n\n"
        return s

if __name__ == '__main__':
    a = SolarInfo()
    b = SolarFlares()
    c = WeatherInfo()

    city = 'Saint-Petersburg'

    a.get_solarinfo_2h()
    b.get_solarflares_6h()
    c.get_weather(city)

    print(a.get_info())
    print(b.get_info())

    print(c.get_info_cur())
    print(c.get_info_forecast())
