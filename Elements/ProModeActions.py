import requests
from requests.exceptions import HTTPError

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
    def takeInfo_NOAA_2h(self):
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
    def takeInfo_NOAA_1d(self):
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
    def takeInfo_NOAA_3d(self):
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
    def takeInfo_NOAA_DST(self):
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
    def takeInfo_NOAA_Kp(self):
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

if __name__ == '__main__':
   #a = SolarInfo()
   #b = SolarInfo()
   #c = SolarInfo()

   ## Получаем информацию по временам полученных измерений за 2 часа
   #a.takeInfo_NOAA_2h()
   #a.takeInfo_NOAA_DST()
   #a.takeInfo_NOAA_Kp()
   #print(" Дата:", len(a.dateBzBt), len(a.bz), len(a.bt), " Дата:", len(a.dateUP), len(a.u), len(a.p), " Дата:", len(a.dateDST), len(a.DST), " Дата:", len(a.dateKp), len(a.Kp), len(a.KpType))

   #b.takeInfo_NOAA_1d()
   #b.takeInfo_NOAA_DST()
   #b.takeInfo_NOAA_Kp()
   #print(" Дата:", len(b.dateBzBt), len(b.bz), len(b.bt), " Дата:", len(b.dateUP), len(b.u), len(b.p), " Дата:", len(b.dateDST), len(b.DST), " Дата:", len(b.dateKp), len(b.Kp), len(b.KpType))

   #c.takeInfo_NOAA_3d()
   #c.takeInfo_NOAA_DST()
   #c.takeInfo_NOAA_Kp()
   #print(" Дата:", len(c.dateBzBt), len(c.bz), len(c.bt), " Дата:", len(c.dateUP), len(c.u), len(c.p), " Дата:", len(c.dateDST), len(c.DST), " Дата:", len(c.dateKp), len(c.Kp), len(c.KpType))

   #del a
   #del b
   #del c
