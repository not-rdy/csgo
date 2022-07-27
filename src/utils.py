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
