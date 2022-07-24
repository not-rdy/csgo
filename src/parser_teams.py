import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm

path_data = '/home/dev/projects/games/csgo/data'

url_main = 'https://www.hltv.org'
url_teams = 'https://www.hltv.org/stats/teams'

r = requests.get(url_teams)
sleep(3)

soup = BeautifulSoup(r.text, 'lxml')
soup = soup.find('body', class_='colsCustom1101')
soup = soup.find('div', class_='bgPadding')
soup = soup.find('div', class_='widthControl')
soup = soup.find('div', class_='colCon')
soup = soup.find('div', class_='contentCol')
soup = soup.find('div', class_='stats-section')
soup = soup.find('table', class_='stats-table player-ratings-table')
soup = soup.find('tbody')
soup = soup.findAll('tr')
teams_list = list(soup)

LIST_team_names = []
LIST_team_flags = []
LIST_team_maps_count = []
LIST_team_kd_diff = []
LIST_team_kd_ratio = []
LIST_team_rating = []
LIST_url_current_team = []
LIST_team_wins_draws_losses = []
LIST_team_total_kills = []
LIST_team_total_deaths = []
LIST_team_rounds_played = []

for team in tqdm(teams_list, total=len(teams_list)):
    team_info = team.findAll('td')

    # собираем статистику по команде на начальной странице
    team_flag = team_info[0].find('img', class_='flag').get('title')
    team_name = team_info[0].find('a').text
    team_maps_count = team_info[1].text
    team_kd_diff = team_info[2].text
    team_kd_ratio = team_info[3].text
    team_rating = team_info[4].text

    # ссылка на страницу команды
    url_current_team = team_info[0].find('a').get('href')
    url_current_team = url_main + url_current_team
    # кидаем запрос и обрабатываем данные со старницы команды
    r = requests.get(url_current_team)
    sleep(3)
    soup = BeautifulSoup(r.text, 'lxml')
    soup = soup.find('body', class_='colsCustom1101')
    soup = soup.find('div', class_='bgPadding')
    soup = soup.find('div', class_='widthControl')
    soup = soup.find('div', class_='colCon')
    soup = soup.find('div', class_='contentCol')
    soup = soup.find(
        'div', class_='stats-section stats-team stats-team-overview'
        )
    rows_of_table = soup.findAll('div', class_='columns')
    # забираем данные из первой строки таблицы
    first_row = rows_of_table[0].\
        findAll('div', class_='col standard-box big-padding')
    team_wins_draws_losses = first_row[1]\
        .find('div', class_='large-strong').text
    team_total_kills = first_row[2]\
        .find('div', class_='large-strong').text
    # забираем данные из второй строки таблицы
    second_row = rows_of_table[1].\
        findAll('div', class_='col standard-box big-padding')
    team_total_deaths = second_row[0]\
        .find('div', class_='large-strong').text
    team_rounds_played = second_row[1]\
        .find('div', 'large-strong').text
    # кладем в листы
    LIST_team_names.append(team_name)
    LIST_team_flags.append(team_flag)
    LIST_team_maps_count.append(team_maps_count)
    LIST_team_kd_diff.append(team_kd_diff)
    LIST_team_kd_ratio.append(team_kd_ratio)
    LIST_team_rating.append(team_rating)
    LIST_url_current_team.append(url_current_team)
    LIST_team_wins_draws_losses.append(team_wins_draws_losses)
    LIST_team_total_kills.append(team_total_kills)
    LIST_team_total_deaths.append(team_total_deaths)
    LIST_team_rounds_played.append(team_rounds_played)

# формируем DataFrame и сохраняем в .csv
df = pd.DataFrame(
    {
        'name': LIST_team_names,
        'flag': LIST_team_flags,
        'maps_count': LIST_team_maps_count,
        'kd_diff': LIST_team_kd_diff,
        'kd_ratio': LIST_team_kd_ratio,
        'rating': LIST_team_rating,
        'url': LIST_url_current_team,
        'wins': [x.split('/')[0] for x in LIST_team_wins_draws_losses],
        'draws': [x.split('/')[1] for x in LIST_team_wins_draws_losses],
        'losses': [x.split('/')[2] for x in LIST_team_wins_draws_losses],
        'total_kills': LIST_team_total_kills,
        'total_deaths': LIST_team_total_deaths,
        'rounds_played': LIST_team_rounds_played
    }
)
df.to_csv(os.path.join(path_data, 'raw', 'teams_stat.csv'))
