from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm
import pandas as pd
import os
import requests
import utils
import dat

DATA_PATH = '/home/dev/projects/games/csgo/data/raw'
url_main = 'https://www.hltv.org/stats/matches?offset='

# итерируемся по страницам со всеми матчами (по 50 матчей на странице)
id_match = 0

for part in tqdm(list(range(0, 50, 50)), total=len(list(range(0, 50, 50)))):
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

    maps_matches = list(map(utils.get_map_match, soup))
    urls_matches = list(map(utils.get_url_match, soup))
    dates_matches = list(map(utils.get_date_match, soup))

    # проваливаемся в каждый матч и собираем информацию
    pbar = tqdm(zip(dates_matches, maps_matches, urls_matches))
    for date_match, map_match, url_match in pbar:

        dat.LIST_date.append(date_match)
        dat.LIST_url_match.append(url_match)

        r = requests.get(url_match)
        sleep(3)
        soup = BeautifulSoup(r.text, 'lxml')

        ####################
        #      первый      #
        ####################
        name_event = utils.get_event_name(soup)
        name_left_team, url_left_team = utils.get_name_and_url_left_team(soup)
        name_right_team, url_right_team = utils\
            .get_name_and_url_right_team(soup)
        breakdown_total, breakdown_left, breakdown_right = utils\
            .get_breakdowns(soup)
        team_rating, first_kills, clutches = utils\
            .get_Rating_FirstKill_Clatches(soup=soup)
        dat.LIST_name_event.append(name_event)
        dat.LIST_left_team.append(name_left_team)
        dat.LIST_url_left_team.append(url_left_team)
        dat.LIST_right_team.append(name_right_team)
        dat.LIST_url_right_team.append(url_right_team)
        dat.LIST_map.append(map_match)
        dat.LIST_breakdown_total.append(breakdown_total)
        dat.LIST_breakdown_left_team.append(breakdown_left)
        dat.LIST_breakdown_right_team.append(breakdown_right)
        dat.LIST_rating.append(team_rating)
        dat.LIST_first_kills.append(first_kills)
        dat.LIST_clutches.append(clutches)

        #########################################
        # игроки с лучшими статистиками за матч #
        #########################################
        most_x = utils.get_most_x_box(soup)
        dat.LIST_most_kills.append(most_x.get('most_kills'))
        dat.LIST_most_damage.append(most_x.get('most_damage'))
        dat.LIST_most_assists.append(most_x.get('most_assists'))
        dat.LIST_most_awp_kills.append(most_x.get('most_awp_kills'))
        dat.LIST_most_first_kills.append(most_x.get('most_first_kills'))
        dat.LIST_best_rating.append(most_x.get('best_rating'))

        ######################
        # история раундов    #
        ######################
        left_rounds_seq, right_rounds_seq = utils\
            .get_rounds_seq(soup)
        dat.LIST_left_rounds_seq.append(left_rounds_seq)
        dat.LIST_right_rounds_seq.append(right_rounds_seq)


df_first_info = pd.DataFrame({
    'date': dat.LIST_date,
    'url_match': dat.LIST_url_match,
    'name_event': dat.LIST_name_event,
    'left_team': dat.LIST_left_team,
    'url_left_team': dat.LIST_url_left_team,
    'right_team': dat.LIST_right_team,
    'url_right_team': dat.LIST_url_right_team,
    'map': dat.LIST_map,
    'breakdown_total': dat.LIST_breakdown_total,
    'breakdown_left_team': dat.LIST_breakdown_left_team,
    'breakdown_right_team': dat.LIST_breakdown_right_team,
    'rating': dat.LIST_rating,
    'first_kills': dat.LIST_first_kills,
    'clutches': dat.LIST_clutches
    })
df_first_info.to_csv(os.path.join(DATA_PATH, 'df_first_info.csv'))

df_best_stats = pd.DataFrame({
    'date': dat.LIST_date,
    'url_match': dat.LIST_url_match,
    'most_kills': dat.LIST_most_kills,
    'most_damage': dat.LIST_most_damage,
    'most_assists': dat.LIST_most_assists,
    'most_awp_kills': dat.LIST_most_awp_kills,
    'most_first_kills': dat.LIST_most_first_kills,
    'best_rating': dat.LIST_best_rating
})
df_best_stats.to_csv(os.path.join(DATA_PATH, 'df_best_stats.csv'))

df_rounds_seq = pd.DataFrame({
    'date': dat.LIST_date,
    'url_match': dat.LIST_url_match,
    'left_rounds_seq': dat.LIST_left_rounds_seq,
    'right_rounds_seq': dat.LIST_right_rounds_seq
    })
df_rounds_seq.to_csv(os.path.join(DATA_PATH, 'df_rounds_seq.csv'))
