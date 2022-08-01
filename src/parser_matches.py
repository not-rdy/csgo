from bs4 import BeautifulSoup
from time import sleep, time
import pandas as pd
import os
import requests
import utils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from user_agent import generate_user_agent

# LISTS
LIST_date = []
LIST_map = []
LIST_url_match = []
# первый
LIST_name_event = []
LIST_left_team = []
LIST_url_left_team = []
LIST_right_team = []
LIST_url_right_team = []
LIST_breakdown_total = []
LIST_breakdown_left_team = []
LIST_breakdown_right_team = []
LIST_rating = []
LIST_first_kills = []
LIST_clutches = []
LIST_round_history_left = []
LIST_round_history_right = []
# игроки с лучшими статистиками за матч
LIST_most_kills = []
LIST_most_damage = []
LIST_most_assists = []
LIST_most_awp_kills = []
LIST_most_first_kills = []
LIST_best_rating = []
# история раундов
LIST_left_rounds_seq = []
LIST_right_rounds_seq = []
# статистики игроков в матчах
LIST_stats_players_both = []
LIST_stats_players_ts = []
LIST_stats_players_ct = []

# data path & url main
DATA_PATH = '/home/dev/projects/games/csgo/data/raw'
url_main = 'https://www.hltv.org/stats/matches?offset='
# error logs path
ERROR_LOGS_PATH = '/home/dev/projects/games/csgo/logs/logs_parser_matches.txt'

# счетчик матчей
num_match = 2000
# счетчики ошибок
num_errors_cookie = 0
both_team_1 = 0
both_team_2 = 0
ts_team_1 = 0
ts_team_2 = 0
ct_team_1 = 0
ct_team_2 = 0

# итерируемся по страницам со всеми матчами (по 50 матчей на странице)
pbar_1 = list(range(2000, 111800, 50))
for part in pbar_1:

    # получаем список из 50 новых матчей
    url_target = url_main + str(part)
    r = requests.get(url_target)
    sleep(5)
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
    pbar_2 = zip(dates_matches, maps_matches, urls_matches)
    for date_match, map_match, url_match in pbar_2:
        num_match += 1
        print(f"ОБРАБАТЫВАЕТСЯ МАТЧ: {num_match}")

        LIST_date.append(date_match)
        LIST_url_match.append(url_match)

        # КИДАЕМ ЗАПРОСЫ
        start = time()
        r = requests.get(url_match)
        sleep(5)
        end = time()
        print(f"Запрос на матч requests: {round(end - start, 2)}")

        # SELENIUM DRIVER
        start = time()
        useragent = generate_user_agent(os=('mac', 'linux'))
        options = Options()
        options.headless = True
        options.add_argument(f"user-agent={useragent}")
        driver = webdriver.Chrome(
            '/home/dev/projects/games/csgo/chromedriver/chromedriver',
            options=options
            )

        # ЗАПРОС НА МАТЧ SELENIUM
        driver.get(url_match)
        sleep(5)
        end = time()
        print(f"Запрос на матч selenium: {round(end - start, 2)}")

        # ПОДТВЕРЖДЕНИЕ cookie
        try:
            start = time()
            v = '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]'
            button_allow_cookie = driver.find_element(
                by=By.XPATH,
                value=v
                )
            button_allow_cookie.click()
            sleep(5)
            end = time()
            print(f"Подтверждение cookie: {round(end - start, 2)}")
        except NoSuchElementException:
            num_errors_cookie += 1
            print("!!!Не нашел кнопку с подтверждением cookie!!!")
            # записываем в лог
            with open(ERROR_LOGS_PATH, 'a', encoding='utf-8') as f:
                f.write(f"\nПОДТВЕРЖДЕНИЕ cookie: {num_errors_cookie}")
            pass

        # ОБРАБОТКА ПОЛУЧЕННОГО ЗАПРОСА В BeautifulSoup
        start = time()
        soup = BeautifulSoup(r.text, 'lxml')
        end = time()
        print(
            f"Обработка полученного запроса в BeautifulSoup:\
{round(end - start, 2)}"
            )

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
        LIST_name_event.append(name_event)
        LIST_left_team.append(name_left_team)
        LIST_url_left_team.append(url_left_team)
        LIST_right_team.append(name_right_team)
        LIST_url_right_team.append(url_right_team)
        LIST_map.append(map_match)
        LIST_breakdown_total.append(breakdown_total)
        LIST_breakdown_left_team.append(breakdown_left)
        LIST_breakdown_right_team.append(breakdown_right)
        LIST_rating.append(team_rating)
        LIST_first_kills.append(first_kills)
        LIST_clutches.append(clutches)

        #########################################
        # игроки с лучшими статистиками за матч #
        #########################################
        most_x = utils.get_most_x_box(soup)
        LIST_most_kills.append(most_x.get('most_kills'))
        LIST_most_damage.append(most_x.get('most_damage'))
        LIST_most_assists.append(most_x.get('most_assists'))
        LIST_most_awp_kills.append(most_x.get('most_awp_kills'))
        LIST_most_first_kills.append(most_x.get('most_first_kills'))
        LIST_best_rating.append(most_x.get('best_rating'))

        ######################
        # история раундов    #
        ######################
        left_rounds_seq, right_rounds_seq = utils\
            .get_rounds_seq(soup)
        LIST_left_rounds_seq.append(left_rounds_seq)
        LIST_right_rounds_seq.append(right_rounds_seq)

        #################################
        # статистики игроков за матч    #
        #################################
        # BOTH side team 1
        try:
            df_stats_players_both_team1 = utils\
                .get_stats_players(
                    driver=driver,
                    date_match=date_match,
                    url_match=url_match,
                    side='both',
                    value_team="""div.stats-content:nth-child(13) > table:nth-child(1) >
                    thead:nth-child(1) > tr:nth-child(1) > th:nth-child(1)""",
                    value_table="""div.stats-content:nth-child(13) >
                    table:nth-child(1) > tbody:nth-child(2)"""
                    )
            LIST_stats_players_both.append(df_stats_players_both_team1)
        except NoSuchElementException:
            print("!!!Не нашел что то в таблице Players Both Team 1!!!")
            both_team_1 += 1
            # записываем в лог
            with open(ERROR_LOGS_PATH, 'a', encoding='utf-8') as f:
                f.write(f"\nBOTH side team 1: {both_team_1}")
            pass
        # BOTH side team 2
        try:
            df_stats_players_both_team2 = utils\
                .get_stats_players(
                    driver=driver,
                    date_match=date_match,
                    url_match=url_match,
                    side='both',
                    value_team="""div.stats-content:nth-child(32) >
                    table:nth-child(1) > thead:nth-child(1) > tr:nth-child(1) >
                    th:nth-child(1)""",
                    value_table="""div.stats-content:nth-child(32) >
                    table:nth-child(1) > tbody:nth-child(2)"""
                    )
            LIST_stats_players_both.append(df_stats_players_both_team2)
        except NoSuchElementException:
            print("!!!Не нашел что то в таблице Players Both Team 2!!!")
            both_team_2 += 1
            # записываем в лог
            with open(ERROR_LOGS_PATH, 'a', encoding='utf-8') as f:
                f.write(f"\nBOTH side team 2: {both_team_2}")
            pass
        # TS side team 1
        try:
            df_stats_players_both_team1 = utils\
                .get_stats_players(
                    driver=driver,
                    date_match=date_match,
                    url_match=url_match,
                    side='ts',
                    value_team="""div.stats-content:nth-child(25) >
                    table:nth-child(1) > thead:nth-child(1) > tr:nth-child(1) >
                    th:nth-child(1)""",
                    value_table="""div.stats-content:nth-child(25) >
                    table:nth-child(1) > tbody:nth-child(2)"""
                    )
            LIST_stats_players_ts.append(df_stats_players_both_team1)
        except NoSuchElementException:
            print("!!!Не нашел что то в таблице Players TS Team 1!!!")
            ts_team_1 += 1
            # записываем в лог
            with open(ERROR_LOGS_PATH, 'a', encoding='utf-8') as f:
                f.write(f"\nTS side team 1: {ts_team_1}")
            pass
        # TS side team 2
        try:
            df_stats_players_both_team2 = utils\
                .get_stats_players(
                    driver=driver,
                    date_match=date_match,
                    url_match=url_match,
                    side='ts',
                    value_team="""div.stats-content:nth-child(44) >
                    table:nth-child(1) > thead:nth-child(1) > tr:nth-child(1) >
                    th:nth-child(1)""",
                    value_table="""div.stats-content:nth-child(44) >
                    table:nth-child(1) > tbody:nth-child(2)"""
                    )
            LIST_stats_players_ts.append(df_stats_players_both_team2)
        except NoSuchElementException:
            print("!!!Не нашел что то в таблице Players TS Team 2!!!")
            ts_team_2 += 1
            # записываем в лог
            with open(ERROR_LOGS_PATH, 'a', encoding='utf-8') as f:
                f.write(f"\nTS side team 2: {ts_team_2}")
            pass
        # CT side team 1
        try:
            df_stats_players_both_team1 = utils\
                .get_stats_players(
                    driver=driver,
                    date_match=date_match,
                    url_match=url_match,
                    side='ct',
                    value_team="""div.stats-content:nth-child(19) >
                    table:nth-child(1) > thead:nth-child(1) > tr:nth-child(1) >
                    th:nth-child(1)""",
                    value_table="""div.stats-content:nth-child(19) >
                    table:nth-child(1) > tbody:nth-child(2)"""
                    )
            LIST_stats_players_ct.append(df_stats_players_both_team1)
        except NoSuchElementException:
            print("!!!Не нашел что то в таблице Players CT Team 1!!!")
            ct_team_1 += 1
            # записываем в лог
            with open(ERROR_LOGS_PATH, 'a', encoding='utf-8') as f:
                f.write(f"\nCT side team 1: {ct_team_1}")
            pass
        # CT side team 2
        try:
            df_stats_players_both_team2 = utils\
                .get_stats_players(
                    driver=driver,
                    date_match=date_match,
                    url_match=url_match,
                    side='ct',
                    value_team="""div.stats-content:nth-child(38) >
                    table:nth-child(1) > thead:nth-child(1) > tr:nth-child(1) >
                    th:nth-child(1)""",
                    value_table="""div.stats-content:nth-child(38) >
                    table:nth-child(1) > tbody:nth-child(2)"""
                    )
            LIST_stats_players_ct.append(df_stats_players_both_team2)
        except NoSuchElementException:
            print("!!!Не нашел что то в таблице Players CT Team 2!!!")
            ct_team_2 += 1
            # записываем в лог
            with open(ERROR_LOGS_PATH, 'a', encoding='utf-8') as f:
                f.write(f"\nCT side team 2: {ct_team_2}")
            pass

        ##########################
        #  Perfomance статистики #
        ##########################
        # ПОТОМ

        # quit chrome
        driver.close()
        driver.quit()

        # save data
        if num_match % 500 == 0:
            ###
            df_first_info = pd.DataFrame({
                'date': LIST_date,
                'url_match': LIST_url_match,
                'name_event': LIST_name_event,
                'left_team': LIST_left_team,
                'url_left_team': LIST_url_left_team,
                'right_team': LIST_right_team,
                'url_right_team': LIST_url_right_team,
                'map': LIST_map,
                'breakdown_total': LIST_breakdown_total,
                'breakdown_left_team': LIST_breakdown_left_team,
                'breakdown_right_team': LIST_breakdown_right_team,
                'rating': LIST_rating,
                'first_kills': LIST_first_kills,
                'clutches': LIST_clutches
                })
            df_first_info.to_csv(
                os.path.join(DATA_PATH, f"{num_match}_df_first_info.csv")
                )
            ###
            df_best_stats = pd.DataFrame({
                'date': LIST_date,
                'url_match': LIST_url_match,
                'most_kills': LIST_most_kills,
                'most_damage': LIST_most_damage,
                'most_assists': LIST_most_assists,
                'most_awp_kills': LIST_most_awp_kills,
                'most_first_kills': LIST_most_first_kills,
                'best_rating': LIST_best_rating
            })
            df_best_stats.to_csv(
                os.path.join(DATA_PATH, f"{num_match}_df_best_stats.csv")
                )
            ###
            df_rounds_seq = pd.DataFrame({
                'date': LIST_date,
                'url_match': LIST_url_match,
                'left_rounds_seq': LIST_left_rounds_seq,
                'right_rounds_seq': LIST_right_rounds_seq
                })
            df_rounds_seq.to_csv(
                os.path.join(DATA_PATH, f"{num_match}_df_rounds_seq.csv")
                )
            ###
            df_stats_players_both = pd.concat(LIST_stats_players_both)\
                .reset_index(drop=True)
            df_stats_players_both.to_csv(
                os.path.join(DATA_PATH, f"{num_match}_df_stats_players_both.csv")
                )
            ###
            df_stats_players_ts = pd.concat(LIST_stats_players_ts)\
                .reset_index(drop=True)
            df_stats_players_ts.to_csv(
                os.path.join(DATA_PATH, f"{num_match}_df_stats_players_ts.csv")
            )
            ###
            df_stats_players_ct = pd.concat(LIST_stats_players_ct)\
                .reset_index(drop=True)
            df_stats_players_ct.to_csv(
                os.path.join(DATA_PATH, f"{num_match}_df_stats_players_ct.csv")
            )
            # ОБНУЛЯЕМ ЛИСТЫ
            LIST_date = []
            LIST_map = []
            LIST_url_match = []
            # первый
            LIST_name_event = []
            LIST_left_team = []
            LIST_url_left_team = []
            LIST_right_team = []
            LIST_url_right_team = []
            LIST_breakdown_total = []
            LIST_breakdown_left_team = []
            LIST_breakdown_right_team = []
            LIST_rating = []
            LIST_first_kills = []
            LIST_clutches = []
            LIST_round_history_left = []
            LIST_round_history_right = []
            # игроки с лучшими статистиками за матч
            LIST_most_kills = []
            LIST_most_damage = []
            LIST_most_assists = []
            LIST_most_awp_kills = []
            LIST_most_first_kills = []
            LIST_best_rating = []
            # история раундов
            LIST_left_rounds_seq = []
            LIST_right_rounds_seq = []
            # статистики игроков в матчах
            LIST_stats_players_both = []
            LIST_stats_players_ts = []
            LIST_stats_players_ct = []
