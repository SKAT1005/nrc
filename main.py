import csv
import json
import os
import shutil
from datetime import datetime, timedelta
from time import sleep
from urllib.request import urlretrieve
from zipfile import ZipFile
from rapidkey import get_key
import requests


BASE_DIR = Path(__file__).resolve().parent.parent
url = "https://binance43.p.rapidapi.com/ticker/24hr"

querystring = {"symbol": "ETHUSDT"}

headers = {
    "X-RapidAPI-Key": get_key(),
    "X-RapidAPI-Host": "binance43.p.rapidapi.com"
}

def delite_files():
    """
    Функция удаляет все файлы в директории,
    чтоб очистить ненужные файлы
    """
    try:
        folder = 'file'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    except:
       pass
 

def get_date():
    """
    Функция получает прошлый и позапрошлый месяц и год для дальнейшей работы
    :return:
        year: год
        mont_one: прошлый месяц
        month_two: позапрошлый месяц
    """
    now = datetime.now()
    two_month = timedelta(60)
    last_month_one = now - timedelta(60)
    last_mont_two = now - timedelta(30)
    year, month_one = str(last_month_one)[:7].split('-')
    month_two = str(last_mont_two)[:7].split('-')[1]
    return str(year), str(month_one), str(month_two)


def get_file(year, month_one, month_two):
    """
    Функция скачивает с API binance 2 архива, с нужной датой,
    после чего добавляет
    их в директорию file и удаляет ненужные архивы

    :param year: Нужный год
    :param month_one: Прошлый месяц
    :param month_two: Позапрошлый месяц
    :return: None
    """
    url = f'https://data.binance.vision/data/spot/monthly/klines/ETHUSDT/1h/ETHUSDT-1h-{year}-{month_one}.zip'
    urlretrieve(url, f'{BASE_DIR}/1.zip')
    with ZipFile('1.zip', 'r') as zip_file:
        zip_file.extractall(f'{BASE_DIR}/file')

    url = f'https://data.binance.vision/data/spot/monthly/klines/ETHUSDT/1h/ETHUSDT-1h-{year}-{month_two}.zip'
    urlretrieve(url, f'{BASE_DIR}/2.zip')
    with ZipFile('2.zip', 'r') as zip_file:
        zip_file.extractall(f'{BASE_DIR}/file')

    os.remove(f'{BASE_DIR}/1.zip')
    os.remove(f'{BASE_DIR}/2.zip')


def get_all_price():
    """
    Функция составляет список из всех цен ETHUSDT за последние два месяца
    :return:
        list_price: список цен ETHUSDT за последние два месяца
    """
    list_price = []
    folder = 'file'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        with open(file_path, newline='') as File:
            reader = csv.reader(File)
            for row in reader:
                list_price.append(float(row[4]))
    return list_price


delite_files()
year, month_one, month_two = get_date()
get_file(year, month_one, month_two)
list_price = get_all_price()
while True:
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    price = float(data['lastPrice'])
    print(f"Цена ETHUSDT={price}")
    count_number = 0
    count_price = 0
    for i in range(len(list_price)-2):
        if price*0.99<=list_price[i]<=price*1.01:
            count_number+=1
            count_price += price - list_price[i+1]
    new_price = price+count_price/count_number
    print(new_price)
    if new_price>=price*1.01:
        print('В течении 60 минут цена вырастет на 1%')
        sleep(3)
