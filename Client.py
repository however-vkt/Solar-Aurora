import asyncio

from aiohttp import ClientSession
from requests.exceptions import HTTPError

####################################################################################################################
#   Класс для элемента "Солнце"
####################################################################################################################
class SolarInfo:
    def __init__(self):
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

    async def get_solarinfo_2h(self):
        async with ClientSession() as session:
            # запрашиваем данные у NOAA
            url = 'http://localhost:8080/solarinfo?tag=s2h'

            async with session.get(url=url) as response:
                try:
                    info = await response.json(content_type='text/plain')
                except HTTPError as http_err:
                    print(f'HTTP error occured: {http_err}')
                except Exception as err:
                    print(f'Other error occured: {err}')
                else:
                    print('Success!')
                    info = await response.json(content_type='text/plain')

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

                    print(info)

    async def get_solarinfo_1d(self):
        async with ClientSession() as session:
            # запрашиваем данные у NOAA
            url = 'http://localhost:8080/solarinfo?tag=s1d'

            async with session.get(url=url) as response:
                try:
                    info = await response.json(content_type='text/plain')
                except HTTPError as http_err:
                    print(f'HTTP error occured: {http_err}')
                except Exception as err:
                    print(f'Other error occured: {err}')
                else:
                    print('Success!')
                    info = await response.json(content_type='text/plain')

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

                    print(info)

    async def get_solarinfo_3d(self):
        async with ClientSession() as session:
            # запрашиваем данные у NOAA
            url = 'http://localhost:8080/solarinfo?tag=s3d'
            dictionary = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}

            async with session.get(url=url) as response:
                try:
                    info = await response.json(content_type='text/plain')
                except HTTPError as http_err:
                    print(f'HTTP error occured: {http_err}')
                except Exception as err:
                    print(f'Other error occured: {err}')
                else:
                    print('Success!')
                    info = await response.json(content_type='text/plain')

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

                    print(info)


####################################################################################################################
#   Класс для элемента "Погода"
####################################################################################################################
class WeatherInfo:
    def __init__(self):
        # Данные собираются с WeatherAPI.com
        self.key = '24c2984466784b7db68124535231004'    # Ключ для работы с сайтом
        self.IP = ''                                    # IP-адрес пользователя

        self.location = dict()
        self.current = dict()

        self.forecast = dict()
        self.history = dict()

    async def get_weather(city):
        async with ClientSession() as session:
            url = f'http://localhost:8080/weather'
            params = {'q': city, 'APPID': 'caca4fd20b8c035ad777a47244d9645e'}

            async with session.get(url=url, params=params) as response:
                weather_json = await response.json()
                try:
                    return weather_json["weather"][0]["main"]
                except KeyError:
                    return 'Нет данных'


####################################################################################################################
#   Класс для элемента "Солнечные вспышки"
####################################################################################################################
class SolarFlares:
    def __init__(self):
        self.date = list()      # Дата измерений
        self.flux = list()      # electron flux

    async def get_solarflares_6h(self):
        async with ClientSession() as session:
            # запрашиваем данные у NOAA
            url = 'http://localhost:8080/flares?tag=s6h'

            async with session.get(url=url) as response:
                try:
                    info = await response.json(content_type='text/plain')
                    # Если ответ успешен, то исключения задействованы не будут
                    response.raise_for_status()

                except HTTPError as http_err:
                    print(f'HTTP error occured: {http_err}')
                except Exception as err:
                    print(f'Other error occured: {err}')
                else:
                    print('Success!')
                    info = await response.json(content_type='text/plain')

                    self.date = info.get('0')
                    self.flux = info.get('1')

                    print(info)

    async def get_solarflares_1d(self):
        async with ClientSession() as session:
            # запрашиваем данные у NOAA
            url = 'http://localhost:8080/flares?tag=s1d'
            dictionary = {0: [], 1: []}

            async with session.get(url=url) as response:
                try:
                    info = await response.json(content_type='text/plain')
                    # Если ответ успешен, то исключения задействованы не будут
                    response.raise_for_status()
                except HTTPError as http_err:
                    print(f'HTTP error occured: {http_err}')
                except Exception as err:
                    print(f'Other error occured: {err}')
                else:
                    print('Success!')
                    info = await response.json(content_type='text/plain')
                    for data in info:
                        dictionary[0].append(data['time_tag'])
                        dictionary[1].append(data['flux'])
                    self.date = dictionary[0]
                    self.flux = dictionary[1]

                    print(self.date)
                    print(self.flux)

    async def get_solarflares_3d(self):
        async with ClientSession() as session:
            # запрашиваем данные у NOAA
            url = 'http://localhost:8080/flares?tag=s3d'
            dictionary = {0: [], 1: []}

            async with session.get(url=url) as response:
                try:
                    info = await response.json(content_type='text/plain')
                    # Если ответ успешен, то исключения задействованы не будут
                    response.raise_for_status()

                except HTTPError as http_err:
                    print(f'HTTP error occured: {http_err}')
                except Exception as err:
                    print(f'Other error occured: {err}')
                else:
                    print('Success!')
                    info = await response.json(content_type='text/plain')

                    for data in info:
                        dictionary[0].append(data['time_tag'])
                        dictionary[1].append(data['flux'])
                    self.date = dictionary[0]
                    self.flux = dictionary[1]

                    print(self.date)
                    print(self.flux)

async def main():
    a = SolarInfo()
    b = SolarFlares()

    while True:
        await a.get_solarinfo_2h()

        await b.get_solarflares_6h()

        print(a.KpType)
        print(a.Kp)

        print(b.date)
        print(b.flux)
        print(" ")
        print(" ")
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())