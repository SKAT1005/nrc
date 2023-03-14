from urllib.request import urlretrieve
from zipfile import ZipFile
import os
url = f'https://data.binance.vision/?prefix=data/spot/monthly/klines/ETHUSDT/1h/ETHUSDT-1h-{year}-{mont_one}.zip'
urlretrieve(url, '/home/admin1/PycharmProjects/pythonProject1/123.zip')
with ZipFile('123.zip', 'r') as zip_file:
    zip_file.extractall('/home/admin1/PycharmProjects/pythonProject1/file')
os.remove('/home/admin1/PycharmProjects/pythonProject1/123.zip')