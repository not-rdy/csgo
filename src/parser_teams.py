import requests
import pandas
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm

url = 'https://www.hltv.org/stats/teams'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
print(soup)
