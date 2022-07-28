def get_map_match(tr_tag):
    Map = tr_tag.find('td', class_='statsDetail')\
        .find('div', class_='dynamic-map-name-full').text
    return Map


def get_url_match(tr_tag):
    url_match = tr_tag.find('td', class_='date-col')\
        .find('a').get('href')
    url_match = 'https://www.hltv.org' + url_match
    return url_match


def get_date_match(tr_tag):
    date_match = tr_tag.find('td', class_='date-col')\
        .find('a').find('div', class_='time').text
    return date_match


def get_event_name(soup):
    soup = soup.find('body', class_='colsCustom1101')
    soup = soup.find('div', class_='bgPadding')
    soup = soup.find('div', class_='widthControl')
    soup = soup.find('div', class_='colCon')
    soup = soup.find('div', class_='contentCol')
    soup = soup.find('div', class_='stats-section stats-match')
    soup = soup.find('div', class_='wide-grid')
    soup = soup.find('div', class_='col match-info-box-col')
    soup = soup.find('div', class_='match-info-box-con')
    soup = soup.find('div', class_='match-info-box')
    name_event = soup.find('a', class_='block text-ellipsis').text
    return name_event


def get_name_and_url_left_team(soup):
    soup = soup.find('body', class_='colsCustom1101')
    soup = soup.find('div', class_='bgPadding')
    soup = soup.find('div', class_='widthControl')
    soup = soup.find('div', class_='colCon')
    soup = soup.find('div', class_='contentCol')
    soup = soup.find('div', class_='stats-section stats-match')
    soup = soup.find('div', class_='wide-grid')
    soup = soup.find('div', class_='col match-info-box-col')
    soup = soup.find('div', class_='match-info-box-con')
    soup = soup.find('div', class_='team-left')
    name_left_team = soup.find('a', class_='block text-ellipsis').text
    url_left_team = soup.find('a', class_='block text-ellipsis')\
        .get('href')
    url_left_team = 'https://www.hltv.org' + url_left_team
    return name_left_team, url_left_team


def get_name_and_url_right_team(soup):
    soup = soup.find('body', class_='colsCustom1101')
    soup = soup.find('div', class_='bgPadding')
    soup = soup.find('div', class_='widthControl')
    soup = soup.find('div', class_='colCon')
    soup = soup.find('div', class_='contentCol')
    soup = soup.find('div', class_='stats-section stats-match')
    soup = soup.find('div', class_='wide-grid')
    soup = soup.find('div', class_='col match-info-box-col')
    soup = soup.find('div', class_='match-info-box-con')
    soup = soup.find('div', class_='team-right')
    name_right_team = soup.find('a', class_='block text-ellipsis').text
    url_right_team = soup.find('a', class_='block text-ellipsis')\
        .get('href')
    url_right_team = 'https://www.hltv.org' + url_right_team
    return name_right_team, url_right_team


def get_breakdowns(soup):
    soup = soup.find('body', class_='colsCustom1101')
    soup = soup.find('div', class_='bgPadding')
    soup = soup.find('div', class_='widthControl')
    soup = soup.find('div', class_='colCon')
    soup = soup.find('div', class_='contentCol')
    soup = soup.find('div', class_='stats-section stats-match')
    soup = soup.find('div', class_='wide-grid')
    soup = soup.find('div', class_='col match-info-box-col')
    soup = soup.find('div', class_='match-info-box-con')
    soup = soup.find('div', class_='match-info-row')
    soup = soup.find('div', class_='right')
    soup = soup.findAll('span')
    counts = [x.text for x in soup]
    sides = [x.get('class') for x in soup]
    breakdown_total = counts[0] + ':' + counts[1]
    breakdown_left = sides[2][0].split('-')[0] + '_' + counts[2] + ':'\
        + sides[3][0].split('-')[0] + '_' + counts[3]
    breakdown_right = sides[4][0].split('-')[0] + '_' + counts[4] + ':'\
        + sides[5][0].split('-')[0] + '_' + counts[5]
    return breakdown_total, breakdown_left, breakdown_right


def get_Rating_FirstKill_Clatches(soup):
    soup = soup.find('body', class_='colsCustom1101')
    soup = soup.find('div', class_='bgPadding')
    soup = soup.find('div', class_='widthControl')
    soup = soup.find('div', class_='colCon')
    soup = soup.find('div', class_='contentCol')
    soup = soup.find('div', class_='stats-section stats-match')
    soup = soup.find('div', class_='wide-grid')
    soup = soup.find('div', class_='col match-info-box-col')
    soup = soup.find('div', class_='match-info-box-con')
    soup = soup.findAll('div', class_='match-info-row')
    soup = [x.find('div', class_='right').text for x in soup[1:]]
    team_rating = soup[0]
    first_kills = soup[1]
    clutches = soup[2]
    return team_rating, first_kills, clutches


def get_most_x_box(soup) -> dict:
    soup = soup.find('body', class_='colsCustom1101')
    soup = soup.find('div', class_='bgPadding')
    soup = soup.find('div', class_='widthControl')
    soup = soup.find('div', class_='colCon')
    soup = soup.find('div', class_='contentCol')
    soup = soup.find('div', class_='stats-section stats-match')
    soup = soup.find('div', class_='wide-grid')
    soup = soup.find('div', class_='col top-players')
    soup = soup.findAll('div', class_='most-x-box standard-box')
    to_return = dict()
    titles = [
        'most_kills', 'most_damage', 'most_assists',
        'most_awp_kills', 'most_first_kills', 'best_rating'
        ]
    for title, most_x in zip(titles, soup):
        name = most_x.find('div', class_='name').find('a').text
        value = most_x.find('div', class_='value').find('span').text
        to_return[title] = name + ':' + value
    return to_return


def get_rounds_seq(soup) -> list:
    soup = soup.find('body', class_='colsCustom1101')
    soup = soup.find('div', class_='bgPadding')
    soup = soup.find('div', class_='widthControl')
    soup = soup.find('div', class_='colCon')
    soup = soup.find('div', class_='contentCol')
    soup = soup.find('div', class_='stats-section stats-match')
    soup = soup.find('div', class_='standard-box round-history-con')
    soup = soup.findAll('div', class_='round-history-team-row')
    left_rounds_seq = soup[0]\
        .findAll('img', class_='round-history-outcome')
    right_rounds_seq = soup[1]\
        .findAll('img', class_='round-history-outcome')
    left_rounds_seq = [
        count.get('title') for count in left_rounds_seq
        ]
    right_rounds_seq = [
        count.get('title') for count in right_rounds_seq
        ]
    return left_rounds_seq, right_rounds_seq
