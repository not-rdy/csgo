import requests
from bs4 import BeautifulSoup
from time import sleep
from utils import get_url_match, get_date_match, get_event_name
from utils import get_name_and_url_left_team, get_name_and_url_right_team

url_main = 'https://www.hltv.org/stats/matches?offset='

# итерируемся по страницам со всеми матчами (по 50 матчей на странице)
LIST_date = []
LIST_url_match = []
LIST_name_event = []
LIST_left_team = []
LIST_url_left_team = []
LIST_right_team = []
LIST_url_right_team = []

id_match = 0

for part in list(range(0, 111800, 50)):
    # получаем список из 50 новых матчей
    url_target = url_main + str(part)
    r = requests.get(url_target)
    sleep(3)
    soup = BeautifulSoup(r.text, 'lxml')

    # формируем перечень ссылок матчей со страницы и даты
    soup = soup.find('body', class_='colsCustom1101')
    soup = soup.find('div', class_='bgPadding')
    soup = soup.find('div', class_='widthControl')
    soup = soup.find('div', class_='colCon')
    soup = soup.find('div', class_='contentCol')
    soup = soup.find('div', class_='stats-section')
    soup = soup.find('table', class_='stats-table matches-table no-sort')
    soup = soup.find('tbody')
    soup = soup.findAll('tr')

    urls_matches = list(map(get_url_match, soup))
    dates_matches = list(map(get_date_match, soup))

    # проваливаемся в каждый матч и собираем информацию
    for date_match, url_match in zip(dates_matches, urls_matches):

        LIST_date.append(date_match)
        LIST_url_match.append(url_match)

        r = requests.get(url_match)
        sleep(3)
        soup = BeautifulSoup(r.text, 'lxml')

        ####################
        # ПЕРВЫЙ ДАТАФРЕЙМ #
        ####################
        # 1) Название эвента
        # 2) Названия команд
        # 3) Ссылки на команды
        # 4) Карта
        # 5) Счет матча
        # 6) Рейтинги команд
        # 7) Количеста первых убийств
        # 8) Clutches won ???

        name_event = get_event_name(soup)
        name_left_team, url_left_team = get_name_and_url_left_team(soup)
        name_right_team, url_right_team = get_name_and_url_right_team(soup)

        LIST_name_event.append(name_event)
        LIST_left_team.append(name_left_team)
        LIST_url_left_team.append(url_left_team)
        LIST_right_team.append(name_right_team)
        LIST_url_right_team.append(url_right_team)

        break
    break
