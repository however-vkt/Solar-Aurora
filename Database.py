from urllib.error import HTTPError

import json
import aiosqlite
import asyncio
from aiohttp import ClientSession, web
from datetime import datetime

########################################################################################################################
#                                               СОЗДАНИЕ БАЗ ДАННЫХ
########################################################################################################################

async def create_table_solarinfo():
    # Создаём Базу данных SolarInfo.db
    async with aiosqlite.connect('SolarInfo.db') as db:
        # Создаём таблицу с данными за 2 часа
        await db.execute('CREATE TABLE IF NOT EXISTS s2h(date TEXT,bz REAL,bt REAL,u REAL,p REAL)')
        await db.commit()

        # Создаём таблицу с данными за 1 день
        await db.execute('CREATE TABLE IF NOT EXISTS s1d(date TEXT,bz REAL,bt REAL,u REAL,p REAL)')
        await db.commit()

        # Создаём таблицу с данными за 3 дня
        await db.execute('CREATE TABLE IF NOT EXISTS s3d(date TEXT,bz REAL,bt REAL,u REAL,p REAL)')
        await db.commit()

        # Создаём таблицу с данными о DST
        await db.execute('CREATE TABLE IF NOT EXISTS sDST(date TEXT, DST REAL)')
        await db.commit()

        # Создаём таблицу с данными о Kp и KpType
        await db.execute('CREATE TABLE IF NOT EXISTS sKp(date TEXT, Kp REAL, KpType TEXT)')
        await db.commit()
async def create_table_weather():
    # Создаём Базу данных Weather.db
    async with aiosqlite.connect('Weather.db') as db:
        # Создаём таблицу с данными о погоде сейчас
        await db.execute('CREATE TABLE IF NOT EXISTS WeatherNow(date TEXT, city TEXT, weather TEXT)')
        await db.commit()

        # Создаём таблицу с данными о прогнозе погоды
        await db.execute('CREATE TABLE IF NOT EXISTS WeatherForecast(date TEXT, city TEXT, weather TEXT)')
        await db.commit()
async def create_table_solarflares():
    # Создаём Базу данных SolarFlares.db
    async with aiosqlite.connect('SolarFlares.db') as db:
        # Создаём таблицу с данными за 6 часов
        await db.execute('CREATE TABLE IF NOT EXISTS s6h(date TEXT, flux REAL)')
        await db.commit()

        # Создаём таблицу с данными за 1 день
        await db.execute('CREATE TABLE IF NOT EXISTS s1d(date TEXT, flux REAL)')
        await db.commit()

        # Создаём таблицу с данными за 3 дня
        await db.execute('CREATE TABLE IF NOT EXISTS s3d(date TEXT, flux REAL)')
        await db.commit()

########################################################################################################################
#                                           СОХРАНЕНИЕ В БАЗЫ ДАННЫХ
########################################################################################################################

async def save_to_solarinfo(tag,
                            dateBzBt, bz, bt, u, p,
                            dateDST, DST,
                            dateKp, Kp, KpType):

    # Подключаемся к базе данных SolarInfo.db
    async with aiosqlite.connect('SolarInfo.db') as db:
        # Добавляем данные за 2 часа
        if tag == 's2h':
            await db.execute("DELETE FROM s2h")
            await db.executemany("INSERT OR IGNORE INTO s2h(date,bz,bt,u,p) VALUES(?,?,?,?,?)",
                                 zip(dateBzBt, bz, bt, u, p))
            await db.commit()

        # Добавляем данные за 1 день
        if tag == 's1d':
            await db.execute("DELETE FROM s1d")
            await db.executemany("INSERT OR IGNORE INTO s1d(date,bz,bt,u,p) VALUES(?,?,?,?,?)",
                                 zip(dateBzBt, bz, bt, u, p))
            await db.commit()

        # Добавляем данные за 3 дня
        if tag == 's3d':
            await db.execute("DELETE FROM s3d")
            await db.executemany("INSERT OR IGNORE INTO s3d(date,bz,bt,u,p) VALUES(?,?,?,?,?)",
                                 zip(dateBzBt, bz, bt, u, p))
            await db.commit()

        # Добавляем данные о DST
        await db.execute("DELETE FROM sDST")
        await db.executemany("INSERT OR IGNORE INTO sDST(date,DST) VALUES(?,?)",
                             zip(dateDST, DST))
        await db.commit()

        # Добавляем данные о Kp и KpType
        await db.execute("DELETE FROM sKp")
        await db.executemany("INSERT OR IGNORE INTO sKp(date,Kp,KpType) VALUES(?,?,?)",
                             zip(dateKp, Kp, KpType))
        await db.commit()
async def save_to_weather(city, weather_now, weather_forecast):
    # Подключаемся к базе данных Weather.db
    async with aiosqlite.connect('Weather.db') as db:
        await db.execute('INSERT INTO WeatherNow VALUES(?,?,?)',
                         (datetime.now(), city, weather_now))
        await db.commit()

        await db.execute('INSERT INTO WeatherForecast VALUES(?,?,?)',
                         (datetime.now(), city, weather_forecast))
        await db.commit()
async def save_to_solarflares(tag, date, flux):
    # Подключаемся к базе данных SolarFlares.db
    async with aiosqlite.connect('SolarFlares.db') as db:
        # Обновляем данные о вспышках за 6 часов
        if tag == 's6h':
            await db.execute("DELETE FROM s6h")
            await db.executemany('INSERT INTO s6h VALUES (?, ?)',
                             zip(date, flux))
            await db.commit()

        # Обновляем данные о вспышках за 1 день
        if tag == 's1d':
            await db.execute("DELETE FROM s1d")
            await db.executemany('INSERT INTO s1d VALUES (?, ?)',
                             zip(date, flux))
            await db.commit()

        # Обновляем данные о вспышках за 3
        if tag == 's3d':
            await db.execute("DELETE FROM s3d")
            await db.executemany('INSERT INTO s3d VALUES (?, ?)',
                             zip(date, flux))
            await db.commit()

########################################################################################################################
#                                               ОБРАБОТКА
########################################################################################################################

async def handle(request):
    city = request.rel_url.query['city']
    print(city)

    # Запись результата
    result = await get_weather(city)

    # Сохранение в базу данных запроса
    #await save_to_weather(city_ru, weather_ru, weather_en)

    # Данные записываются в ветвь
    return web.Response(text=json.dumps(dict(result), ensure_ascii=False))
async def handle_solarinfo(request):
    tag = request.rel_url.query['tag']
    print(tag)
    result = dict()
    if tag == 's2h':
        result = await get_solarinfo_2h()

    if tag == 's1d':
        result = await get_solarinfo_1d()

    if tag == 's3d':
        result = await get_solarinfo_3d()

    # Сохранение в базу данных запроса
    await save_to_solarinfo(tag, list(result[0]), list(result[1]), list(result[2]), list(result[3]), list(result[4]),
                            list(result[5]), list(result[6]), list(result[7]), list(result[8]), list(result[9]))

    # Данные записываются в ветвь
    return web.Response(text=json.dumps(dict(result), ensure_ascii=False))
async def handle_solarflares(request):
    tag = request.rel_url.query['tag']
    print(tag)
    result = dict()
    if tag == 's6h':
        result = await get_solarflares_6h()

    if tag == 's1d':
        result = await get_solarflares_1d()

    if tag == 's3d':
        result = await get_solarflares_3d()

    # Сохранение в базу данных запроса
    await save_to_solarflares(tag, list(result[0]), list(result[1]))
    # Данные записываются в ветвь
    return web.Response(text=json.dumps(dict(result), ensure_ascii=False))

########################################################################################################################
#                                           ПОЛУЧЕНИЕ ДАННЫХ
########################################################################################################################

async def get_weather(city):
    async with ClientSession() as session:
        url = f'http://api.weatherapi.com/v1/forecast.json'
        key = '24c2984466784b7db68124535231004'

        params = {'key': key, 'q':[city], 'days': '1', 'aqi': ['no'], 'alerts': ['no']}

        dictionary = {0: [], 1: [], 2: []}
        async with session.get(url=url, params=params) as response:
            try:
                info = await response.json()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                info = await response.json()

                # Организуем данные в словарь
                dictionary[0] = info['location']
                dictionary[1] = info['current']
                dictionary[2] = info['forecast']
    return dictionary

async def get_solarinfo_2h():
    async with ClientSession() as session:
        # запрашиваем данные у NOAA
        url = 'https://services.swpc.noaa.gov/products/solar-wind/mag-2-hour.json'
        dictionary = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}

        async with session.get(url=url) as response:
            try:
                info = await response.json()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')
                info = await response.json()

                # Организуем данные в словарь
                flag = 0
                for data in info:
                    if flag != 0:
                        dictionary[0].append(data[0])
                        dictionary[1].append(data[3])
                        dictionary[2].append(data[6])
                    flag = 1

        # запрашиваем данные у NOAA
        url = 'https://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json'
        async with session.get(url=url) as response:
            try:
                info = await response.json()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                info = await response.json()

                # Организуем данные в словарь
                flag = 0
                for data in info:
                    if flag != 0:
                        dictionary[3].append(data[1])
                        dictionary[4].append(data[2])
                    flag = 1
        url = 'https://services.swpc.noaa.gov/products/kyoto-dst.json'
        async with session.get(url=url) as response:
            try:
                info = await response.json()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                info = await response.json()

                # Организуем данные в словарь
                flag = 0
                for data in info:
                    if flag != 0:
                        dictionary[5].append(data[0])
                        dictionary[6].append(data[1])
                    flag = 1
        url = 'https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json'
        async with session.get(url=url) as response:
            try:
                info = await response.json()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                info = await response.json()

                # Организуем данные в словарь
                flag = 0
                for data in info:
                    if flag != 0:
                        dictionary[7].append(data[0])
                        dictionary[8].append(data[1])
                        dictionary[9].append(data[2])
                    flag = 1
    # dict[0] - dateBzBt
    # dict[1] - bz
    # dict[2] - bt
    # dict[3] - u
    # dict[4] - p

    # dict[5] - dateDST
    # dict[6] - DST
    # dict[7] - dateKp
    # dict[8] - Kp
    # dict[9] - KpType
    return dictionary
async def get_solarinfo_1d():
    async with ClientSession() as session:
        # запрашиваем данные у NOAA
        url = 'https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json'
        dictionary = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}

        async with session.get(url=url) as response:
            try:
                info = await response.json()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')
                info = await response.json()

                # Организуем данные в словарь
                flag = 0
                for data in info:
                    if flag != 0:
                        dictionary[0].append(data[0])
                        dictionary[1].append(data[3])
                        dictionary[2].append(data[6])
                    flag = 1

        # запрашиваем данные у NOAA
        url = 'https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json'
        async with session.get(url=url) as response:
            try:
                info = await response.json()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                info = await response.json()

                # Организуем данные в словарь
                flag = 0
                for data in info:
                    if flag != 0:
                        dictionary[3].append(data[1])
                        dictionary[4].append(data[2])
                    flag = 1
        url = 'https://services.swpc.noaa.gov/products/kyoto-dst.json'
        async with session.get(url=url) as response:
            try:
                info = await response.json()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                info = await response.json()

                # Организуем данные в словарь
                flag = 0
                for data in info:
                    if flag != 0:
                        dictionary[5].append(data[0])
                        dictionary[6].append(data[1])
                    flag = 1
        url = 'https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json'
        async with session.get(url=url) as response:
            try:
                info = await response.json()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                info = await response.json()

                # Организуем данные в словарь
                flag = 0
                for data in info:
                    if flag != 0:
                        dictionary[7].append(data[0])
                        dictionary[8].append(data[1])
                        dictionary[9].append(data[2])
                    flag = 1
    # dict[0] - dateBzBt
    # dict[1] - bz
    # dict[2] - bt
    # dict[3] - u
    # dict[4] - p

    # dict[5] - dateDST
    # dict[6] - DST
    # dict[7] - dateKp
    # dict[8] - Kp
    # dict[9] - KpType
    return dictionary
async def get_solarinfo_3d():
    async with ClientSession() as session:
        # запрашиваем данные у NOAA
        url = 'https://services.swpc.noaa.gov/products/solar-wind/mag-3-day.json'
        dictionary = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}

        async with session.get(url=url) as response:
            try:
                info = await response.json()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')
                info = await response.json()

                # Организуем данные в словарь
                flag = 0
                for data in info:
                    if flag != 0:
                        dictionary[0].append(data[0])
                        dictionary[1].append(data[3])
                        dictionary[2].append(data[6])
                    flag = 1

        # запрашиваем данные у NOAA
        url = 'https://services.swpc.noaa.gov/products/solar-wind/plasma-3-day.json'
        async with session.get(url=url) as response:
            try:
                info = await response.json()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                info = await response.json()

                # Организуем данные в словарь
                flag = 0
                for data in info:
                    if flag != 0:
                        dictionary[3].append(data[1])
                        dictionary[4].append(data[2])
                    flag = 1
        url = 'https://services.swpc.noaa.gov/products/kyoto-dst.json'
        async with session.get(url=url) as response:
            try:
                info = await response.json()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                info = await response.json()

                # Организуем данные в словарь
                flag = 0
                for data in info:
                    if flag != 0:
                        dictionary[5].append(data[0])
                        dictionary[6].append(data[1])
                    flag = 1
        url = 'https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json'
        async with session.get(url=url) as response:
            try:
                info = await response.json()
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')

                info = await response.json()

                # Организуем данные в словарь
                flag = 0
                for data in info:
                    if flag != 0:
                        dictionary[7].append(data[0])
                        dictionary[8].append(data[1])
                        dictionary[9].append(data[2])
                    flag = 1
    # dict[0] - dateBzBt
    # dict[1] - bz
    # dict[2] - bt
    # dict[3] - u
    # dict[4] - p

    # dict[5] - dateDST
    # dict[6] - DST
    # dict[7] - dateKp
    # dict[8] - Kp
    # dict[9] - KpType
    return dictionary

async def get_solarflares_6h():
    async with ClientSession() as session:
        # запрашиваем данные у NOAA
        url = 'https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json'
        dictionary = {0: [], 1: []}

        async with session.get(url=url) as response:
            try:
                info = await response.json()
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')
                info = await response.json()
                for data in info:
                    dictionary[0].append(data['time_tag'])
                    dictionary[1].append(data['flux'])
    return dictionary
async def get_solarflares_1d():
    async with ClientSession() as session:
        # запрашиваем данные у NOAA
        url = 'https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json'
        dictionary = {0: [], 1: []}

        async with session.get(url=url) as response:
            try:
                info = await response.json()
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')
                info = await response.json()
                for data in info:
                    dictionary[0].append(data['time_tag'])
                    dictionary[1].append(data['flux'])
    return dictionary
async def get_solarflares_3d():
    async with ClientSession() as session:
        # запрашиваем данные у NOAA
        url = 'https://services.swpc.noaa.gov/json/goes/primary/xrays-3-day.json'
        dictionary = {0: [], 1: []}

        async with session.get(url=url) as response:
            try:
                info = await response.json()
                # Если ответ успешен, то исключения задействованы не будут
                response.raise_for_status()

            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured: {err}')
            else:
                print('Success!')
                info = await response.json()
                for data in info:
                    dictionary[0].append(data['time_tag'])
                    dictionary[1].append(data['flux'])
    return dictionary

########################################################################################################################
#                                           Основная программа
########################################################################################################################

async def main():
    await create_table_solarinfo()
    await create_table_solarflares()
    #await create_table_weather()

    # создание сервера
    app = web.Application()
    # создание веток
    app.add_routes([web.get('/weather', handle)])
    app.add_routes([web.get('/solarinfo', handle_solarinfo)])
    app.add_routes([web.get('/flares', handle_solarflares)])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

    while True:
        await asyncio.sleep(7200)

if __name__ == '__main__':
    asyncio.run(main())