import asyncio

from aiohttp import ClientSession, ClientConnectorError


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
            try:
                # запрашиваем данные у NOAA
                url = 'http://localhost:8080/solarinfo?tag=s2h'
                async with session.get(url=url) as response:
                    try:
                        info = await response.json(content_type='text/plain')

                    except ClientConnectorError as client_err:
                        print(f'HTTP error occured: {client_err}')
                        return client_err
                    except Exception as err:
                        print(f'Other error occured: {err}')
                        return err
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
                    return info
            except Exception as conn_err:
                print(f'HTTP error occured: {conn_err}')
                return conn_err
    async def get_solarinfo_1d(self):
        async with ClientSession() as session:
            try:
                # запрашиваем данные у NOAA
                url = 'http://localhost:8080/solarinfo?tag=s1d'

                async with session.get(url=url) as response:
                    try:
                        info = await response.json(content_type='text/plain')

                    except ClientConnectorError as client_err:
                        print(f'HTTP error occured: {client_err}')
                        return client_err
                    except Exception as err:
                        print(f'Other error occured: {err}')
                        return err
                    else:
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
                        return info

            except Exception as conn_err:
                print(f'HTTP error occured: {conn_err}')
                return conn_err
    async def get_solarinfo_3d(self):
        async with ClientSession() as session:
            try:
                # запрашиваем данные у NOAA
                url = 'http://localhost:8080/solarinfo?tag=s3d'

                async with session.get(url=url) as response:
                    try:
                        info = await response.json(content_type='text/plain')

                    except ClientConnectorError as client_err:
                        print(f'HTTP error occured: {client_err}')
                        return client_err
                    except Exception as err:
                        print(f'Other error occured: {err}')
                        return err
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
                        return info

            except Exception as conn_err:
                print(f'HTTP error occured: {conn_err}')
                return conn_err

####################################################################################################################
#   Класс для элемента "Погода"
####################################################################################################################
#
#                                           ЗАПИСАТЬ ДАННЫЕ!!!!!
class WeatherInfo:
    def __init__(self):
        # Данные собираются с WeatherAPI.com
        self.location = dict()
        self.current = dict()
        self.forecast = dict()

    async def get_weather(self, city):
        async with ClientSession() as session:
            try:
                print(city)

                url = f'http://localhost:8080/weather'
                params ={'city': city}
                async with session.get(url=url, params=params) as response:
                    try:
                        info = await response.json(content_type='text/plain')
                        # Если ответ успешен, то исключения задействованы не будут
                        response.raise_for_status()

                    except ClientConnectorError as client_err:
                        print(f'HTTP error occured: {client_err}')
                        return client_err
                    except Exception as err:
                        print(f'Other error occured: {err}')
                        return err
                    else:
                        print('Success!')
                        info = await response.json(content_type='text/plain')

                        self.location = info.get('0')
                        self.current = info.get('1')
                        self.forecast = info.get('2')

                        print(self.location)
                        print(self.current)
                        print(self.forecast)
                        info = {'location': self.location, 'current': self.current, 'forecast':self.forecast}
                        return info

            except Exception as conn_err:
                print(f'HTTP error occured: {conn_err}')
                return conn_err

####################################################################################################################
#   Класс для элемента "Солнечные вспышки"
####################################################################################################################
class SolarFlares:
    def __init__(self):
        self.date = list()      # Дата измерений
        self.flux = list()      # electron flux

    async def get_solarflares_6h(self):
        async with ClientSession() as session:
            try:
                # запрашиваем данные у NOAA
                url = 'http://localhost:8080/flares?tag=s6h'

                async with session.get(url=url) as response:
                    try:
                        info = await response.json(content_type='text/plain')
                        # Если ответ успешен, то исключения задействованы не будут
                        response.raise_for_status()

                    except ClientConnectorError as client_err:
                        print(f'HTTP error occured: {client_err}')
                        return client_err
                    except Exception as err:
                        print(f'Other error occured: {err}')
                        return err
                    else:
                        print('Success!')
                        info = await response.json(content_type='text/plain')

                        self.date = info.get('0')
                        self.flux = info.get('1')
                        print(info)
                        return info

            except Exception as conn_err:
                print(f'HTTP error occured: {conn_err}')
                return conn_err
    async def get_solarflares_1d(self):
        async with ClientSession() as session:
            try:
                # запрашиваем данные у NOAA
                url = 'http://localhost:8080/flares?tag=s1d'
                dictionary = {0: [], 1: []}

                async with session.get(url=url) as response:
                    try:
                        info = await response.json(content_type='text/plain')
                        # Если ответ успешен, то исключения задействованы не будут
                        response.raise_for_status()

                    except ClientConnectorError as client_err:
                        print(f'HTTP error occured: {client_err}')
                        return client_err
                    except Exception as err:
                        print(f'Other error occured: {err}')
                        return err
                    else:
                        print('Success!')
                        info = await response.json(content_type='text/plain')

                        self.date = info.get('time_tag')
                        self.flux = info.get('flux')

                        print(self.date)
                        print(self.flux)
                        return info

            except Exception as conn_err:
                print(f'HTTP error occured: {conn_err}')
                return conn_err
    async def get_solarflares_3d(self):
        async with ClientSession() as session:
            try:
                # запрашиваем данные у NOAA
                url = 'http://localhost:8080/flares?tag=s3d'
                dictionary = {0: [], 1: []}

                async with session.get(url=url) as response:
                    try:
                        info = await response.json(content_type='text/plain')
                        # Если ответ успешен, то исключения задействованы не будут
                        response.raise_for_status()

                    except ClientConnectorError as client_err:
                        print(f'HTTP error occured: {client_err}')
                        return client_err
                    except Exception as err:
                        print(f'Other error occured: {err}')
                        return err
                    else:
                        print('Success!')
                        info = await response.json(content_type='text/plain')

                        self.date = info.get('time_tag')
                        self.flux = info.get('flux')

                        print(self.date)
                        print(self.flux)
                        return info

            except Exception as conn_err:
                print(f'HTTP error occured: {conn_err}')
                return conn_err

async def main():
    a = SolarInfo()
    b = SolarFlares()
    c = WeatherInfo()

    # Асинхронное обновление данных
    while True:
        await a.get_solarinfo_2h()

        await b.get_solarflares_6h()

        city = 'Saint-Petersburg'
        await c.get_weather(city)

        print(a.KpType)
        print(a.Kp)
        print(" ")

        print(b.date)
        print(b.flux)
        print(" ")

        print(c.location)
        print(c.current)
        print(c.forecast)
        print(" ")
        print(" ")
        await asyncio.sleep(7200)

if __name__ == '__main__':
    asyncio.run(main())