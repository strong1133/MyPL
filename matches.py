from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver

client = MongoClient('mongodb://tjrwls455:3879@13.125.246.107', 27017)
db = client.epls

chrome_driver_dir = './static/bin/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
driver = webdriver.Chrome(chrome_driver_dir,
                          chrome_options=chrome_options)  # Optional argument, if not specified will search path.
driver.get('https://sports.news.naver.com/wfootball/schedule/index.nhn?year=2021&month=01&category=epl');

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


def insert_schedules():
    trs = soup.select('#_monthlyScheduleList > tr')

    for tr in trs:
        days = tr.select_one('th > div')

        # 경기유무/경기시간
        time = tr.select_one('td.time_place > div > span.time')
        if time is None:
            t = '경기가 없습니다.'
        else:
            t = time.text

        # 경기날짜
        if days is not None:
            a = days.text.strip().split(' ')
            day = a[0]
            days_of_weekend = a[1]
        else:
            day = "no_match_day"
            days_of_weekend = "no_match"

        # 경기장소
        place = tr.select_one('td.time_place > div > span.place')
        if place is not None:
            place = place.text
        else:
            place = "no_match"

        # home_team
        home_team = tr.select_one('div > span.team_left > span.name')
        if home_team is not None:
            home_team = home_team.text
        else:
            home_team = "no_match"

        # away_team
        away_team = tr.select_one('div > span.team_right > span.name')
        if away_team is not None:
            away_team = away_team.text
        else:
            away_team = "no_match"

        # home_team-home_team_score
        home_team_score = tr.select_one('div > span.team_left > span.score')
        if home_team_score is not None:
            home_team_score = home_team_score.text
        else:
            home_team_score = "경기 시작 전"

        # away_team_score
        away_team_score = tr.select_one('div > span.team_right > span.score')
        if away_team_score is not None:
            away_team_score = away_team_score.text
        else:
            away_team_score = "before_match"

        # home_team_emblem
        home_team_emblem = tr.select_one('div > span.team_left > img')
        if home_team_emblem is None:
            home_team_emblem = " "
        else:
            home_team_emblem = home_team_emblem['src']
            # img_url 추출
            emblem_b = home_team_emblem.split('=')
            emblem_c = emblem_b[1].split('&')
            home_team_emblem = emblem_c[0]

        # away_team_emblem
        away_team_emblem = tr.select_one('div > span.team_right > img')
        if away_team_emblem is None:
            away_team_emblem = " "
        else:
            away_team_emblem = away_team_emblem['src']
            # img_url 추출
            emblem_b = away_team_emblem.split('=')
            emblem_c = emblem_b[1].split('&')
            away_team_emblem = emblem_c[0]

        # match_detail_link
        match_detail_link = tr.select_one('td.broadcast > div > a')
        if match_detail_link is not None:
            match_detail_link = match_detail_link['href']
        else:
            match_detail_link = "경기가 없습니다."
        # 딕셔너리 저장/DB 준비
        epl_schedules = {
            'date': day,
            'day_of_the_week': days_of_weekend,
            'match_times': [t],
            'place': place,
            'home_team': home_team,
            'away_team': away_team,
            'home_team_score': home_team_score,
            'away_team_score': away_team_score,
            'home_team_emblem': home_team_emblem,
            'away_team_emblem': away_team_emblem,
            'match_detail_link': match_detail_link
        }
        db.schedules.insert_one(epl_schedules)


def schedules_insert_all():
    db.schedules.drop()
    insert_schedules()
    driver.quit()



schedules_insert_all()
