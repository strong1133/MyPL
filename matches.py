from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver

client = MongoClient('localhost', 27017)
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

        # 경기장소
        place = tr.select_one('td.time_place > div > span.place')
        if place is not None:
            place = place.text

        # home_team
        home_team = tr.select_one('div > span.team_left > span.name')
        if home_team is not None:
            home_team = home_team.text

        # away_team
        away_team = tr.select_one('div > span.team_right > span.name')
        if away_team is not None:
            away_team = away_team.text

        # home_team-home_team_score
        home_team_score = tr.select_one('div > span.team_left > span.score')
        if home_team_score is not None:
            home_team_score = home_team_score.text

        # away_team_score
        away_team_score = tr.select_one('div > span.team_right > span.score')
        if away_team_score is not None:
            away_team_score = away_team_score.text

        # home_team_emblem
        home_team_emblem = tr.select_one('div > span.team_left > img')
        if home_team_emblem is not None:
            home_team_emblem = home_team_emblem['src']
            # img_url 추출
            emblem_b = home_team_emblem.split('=')
            emblem_c = emblem_b[1].split('&')
            home_team_emblem = emblem_c[0]

        # away_team_emblem
        away_team_emblem = tr.select_one('div > span.team_right > img')
        if away_team_emblem is not None:
            away_team_emblem = away_team_emblem['src']
            # img_url 추출
            emblem_b = away_team_emblem.split('=')
            emblem_c = emblem_b[1].split('&')
            away_team_emblem = emblem_c[0]

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
            'away_team_emblem': away_team_emblem
        }
        db.schedules.insert_one(epl_schedules)


def insert_all():
    db.schedules.drop()
    insert_schedules()
    driver.quit()


insert_all()
