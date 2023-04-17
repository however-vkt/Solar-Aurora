import requests
from requests.exceptions import HTTPError

# Класс для элемента "Солнце"
class SolarInfo:
    def __init__(self):
        self.dateBzBt = list()  # Дата со спутника (для bz, bt)
        self.dateUP = list()    # Дата со спутника (для u, p)
        self.dateDST = list()   # Дата для DST
        self.dateKp = list()    # Дата для Kp

        self.bz = list()        # Bz-компонента     [nT]
        self.bt = list()        # Межпланетное магнитное поле (IMF) [nT]
        self.u = list()         # Скорость солнечного ветра [км/с]
        self.p = list()         # Плотность потока  [p/см3]
        self.DST = list()       # Индекс временного спада   [nT]
        self.Kp = list()        # Kp-индекс
        self.KpType = list()    # Тип Kp-индекса (observed, estimated, predicted)
    # Функция получения и сортировки данных от NOAA SWPC за 2 часа (date, bz, bt, date2, u, p)
    def get_2h(self):
        #запрашиваем данные у NOAA
        for url in ['https://services.swpc.noaa.gov/products/solar-wind/mag-2-hour.json']:
            try:
                response = requests.get(url)
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                response = requests.get('https://services.swpc.noaa.gov/products/solar-wind/mag-2-hour.json')
                info = response.json()

                # Организуем данные в словарь
                flag = 0
                dict = {0: [], 1: [], 2: []}
                for data in info:
                    if flag != 0:
                        dict[0].append(data[0])
                        dict[1].append(data[3])
                        dict[2].append(data[6])
                    flag = 1

                # Организуем списки с отсортированными данными (date, bz, bt)
                self.dateBzBt = list(dict[0])
                self.bz = list(dict[1])
                self.bt = list(dict[2])

        # Запрашиваем данные у NOAA
        for url in ['https://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json']:
            try:
                response = requests.get(url)
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                response = requests.get('https://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json')
                info = response.json()

                # Организуем данные в словарь
                flag = 0
                dict = {0: [], 1: [], 2: []}
                for data in info:
                    if flag != 0:
                        dict[0].append(data[0])
                        dict[1].append(data[1])
                        dict[2].append(data[2])
                    flag = 1

                # Организуем списки с отсортированными данными (date, u, p)
                self.dateUP = list(dict[0])
                self.u = list(dict[1])
                self.p = list(dict[2])
    # Функция получения и сортировки данных от NOAA SWPC за 1 день (date, bz, bt, date2, u, p)
    def get_1d(self):
        # Запрашиваем данные у NOAA
        for url in ['https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json']:
            try:
                response = requests.get(url)
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                response = requests.get('https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json')
                info = response.json()

                # Организуем данные в словарь
                flag = 0
                dict = {0: [], 1: [], 2: []}
                for data in info:
                    if flag != 0:
                        dict[0].append(data[0])
                        dict[1].append(data[3])
                        dict[2].append(data[6])
                    flag = 1

                # Организуем списки с отсортированными данными (date, bz, bt)
                self.dateBzBt = list(dict[0])
                self.bz = list(dict[1])
                self.bt = list(dict[2])

        # Запрашиваем данные у NOAA
        for url in ['https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json']:
            try:
                response = requests.get(url)
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                response = requests.get('https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json')
                info = response.json()

                # Организуем данные в словарь
                flag = 0
                dict = {0: [], 1: [], 2: []}
                for data in info:
                    if flag != 0:
                        dict[0].append(data[0])
                        dict[1].append(data[1])
                        dict[2].append(data[2])
                    flag = 1

                # Организуем списки с отсортированными данными (date, u, p)
                self.dateUP = list(dict[0])
                self.u = list(dict[1])
                self.p = list(dict[2])
    # Функция получения и сортировки данных от NOAA SWPC за 3 дня (date, bz, bt, date2, u, p)
    def get_3d(self):
        # Запрашиваем данные у NOAA
        for url in ['https://services.swpc.noaa.gov/products/solar-wind/mag-3-day.json']:
            try:
                response = requests.get(url)
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                response = requests.get('https://services.swpc.noaa.gov/products/solar-wind/mag-3-day.json')
                info = response.json()

                # Организуем данные в словарь
                flag = 0
                dict = {0: [], 1: [], 2: []}
                for data in info:
                    if flag != 0:
                        dict[0].append(data[0])
                        dict[1].append(data[3])
                        dict[2].append(data[6])
                    flag = 1

                # Организуем списки с отсортированными данными (date, bz, bt)
                self.dateBzBt = list(dict[0])
                self.bz = list(dict[1])
                self.bt = list(dict[2])

        # Запрашиваем данные у NOAA
        for url in ['https://services.swpc.noaa.gov/products/solar-wind/plasma-3-day.json']:
            try:
                response = requests.get(url)
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                response = requests.get('https://services.swpc.noaa.gov/products/solar-wind/plasma-3-day.json')
                info = response.json()

                # Организуем данные в словарь
                flag = 0
                dict = {0: [], 1: [], 2: []}
                for data in info:
                    if flag != 0:
                        dict[0].append(data[0])
                        dict[1].append(data[1])
                        dict[2].append(data[2])
                    flag = 1

                # Организуем списки с отсортированными данными (date, u, p)
                self.dateUP = list(dict[0])
                self.u = list(dict[1])
                self.p = list(dict[2])
    # Функция получения и сортировки данных от NOAA SWPC (DST)
    def get_DST(self):
        # Запрашиваем данные у NOAA
        for url in ['https://services.swpc.noaa.gov/products/kyoto-dst.json']:
            try:
                response = requests.get(url)
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                response = requests.get('https://services.swpc.noaa.gov/products/kyoto-dst.json')
                info = response.json()

                # Организуем данные в словарь
                flag = 0
                dict = {0: [], 1: [], 2: []}
                for data in info:
                    if flag != 0:
                        dict[0].append(data[0])
                        dict[1].append(data[1])
                    flag = 1

                # Организуем списки с отсортированными данными (date, DST)
                self.dateDST = list(dict[0])
                self.DST = list(dict[1])
    # Функция получения и сортировки данных от NOAA SWPC (Kp)
    def get_Kp(self):
        # Запрашиваем данные у NOAA
        for url in ['https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json']:
            try:
                response = requests.get(url)
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                response = requests.get('https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json')
                info = response.json()

                # Организуем данные в словарь
                flag = 0
                dict = {0: [], 1: [], 2: []}
                for data in info:
                    if flag != 0:
                        dict[0].append(data[0])
                        dict[1].append(data[1])
                        dict[2].append(data[2])
                    flag = 1

                # Организуем списки с отсортированными данными (date, kp, kptype)
                self.dateKp = list(dict[0])
                self.Kp = list(dict[1])
                self.KpType = list(dict[2])

# Класс для элемента "Погода"
class WeatherInfo:
    def __init__(self):
        # Данные собираются с   WeatherAPI.com
        self.key = '24c2984466784b7db68124535231004'    # Ключ для работы с сайтом
        self.IP = ''                                    # IP-адрес пользователя

        self.location = dict()
        self.current = dict()

        self.forecast = dict()
        self.history = dict()

    # Получение IP-адреса пользователя
    def get_IP(self):
        for url in ['https://ifconfig.me/ip']:
            try:
                response = requests.get(url)
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')
                self.IP = requests.get('https://ifconfig.me/ip').text
                print('IP getted:', self.IP)

    # Получение информации по погоде с помощью IP-адреса (для автоопределения)
    def get_CurrentWeather_IP(self):
        params = {'key': self.key, 'q': [self.IP]}
        response = requests.get('http://api.weatherapi.com/v1/current.json', params=params)
        info = response.json()

        self.location = info['location']
        self.current = info['current']

        print(self.location)
        print(self.current)

        self.location.clear()
        self.current.clear()
    def get_ForecastWeather_IP(self):
        days = 1
        params = {'key': self.key, 'q':[self.IP], 'days': days, 'aqi': ['no'], 'alerts': ['no']}
        response = requests.get('http://api.weatherapi.com/v1/forecast.json', params=params)

        ################################################################################################################
        # Слишком большой объем, который можно распределить сразу между location(dict), current(dict), forecast(dict)
        ################################################################################################################
        info = response.json()

        print(info)

        self.location = info['location']
        self.current = info['current']
        self.forecast = info['forecast']

        print(len(self.location))
        print(len(self.current))
        print(len(self.forecast))

        self.location.clear()
        self.current.clear()
        self.forecast.clear()
    # Получение ID местоположения с помощью поиска (по городу, району, области, стране, аэропорту)
    #def get_WeatherInfo_Query(self):


# Класс для элемента "Солнечные вспышки"
class SolarFlares:
    def __init__(self):
        self.date = list()      # Дата измерений
        self.flux = list()      # electron flux

    # Информация об electron flux за 6 часов
    def get_6h(self):
        #запрашиваем данные у NOAA
        for url in ['https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json']:
            try:
                response = requests.get(url)
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')
                response = requests.get('https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json')
                info = response.json()
                for data in info:
                    self.date.append(data['time_tag'])
                    self.flux.append(data['flux'])

    # Информация об electron flux за 1 день
    def get_1d(self):
        #запрашиваем данные у NOAA
        for url in ['https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json']:
            try:
                response = requests.get(url)
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')
                response = requests.get('https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json')
                info = response.json()
                for data in info:
                    self.date.append(data['time_tag'])
                    self.flux.append(data['flux'])

    # Информация об electron flux за 3 дня
    def get_3d(self):
        #запрашиваем данные у NOAA
        for url in ['https://services.swpc.noaa.gov/json/goes/primary/xrays-3-day.json']:
            try:
                response = requests.get(url)
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')
                response = requests.get('https://services.swpc.noaa.gov/json/goes/primary/xrays-3-day.json')
                info = response.json()
                for data in info:
                    self.date.append(data['time_tag'])
                    self.flux.append(data['flux'])

if __name__ == '__main__':
    a = WeatherInfo()
    a.get_IP()
    a.get_CurrentWeather_IP()
    a.get_ForecastWeather_IP()
