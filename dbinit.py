from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

chrome_driver_dir = './static/bin/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

driver = webdriver.Chrome(chrome_driver_dir,
                          chrome_options=chrome_options)  # Optional argument, if not specified will search path.
driver.get('https://sports.news.naver.com/wfootball/record/index.nhn');

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


def insert_tables():
    trs = soup.select('#wfootballTeamRecordBody > table > tbody > tr')
    rank = 0

    for tr in trs:
        rank += 1
        emblem_a = tr.select_one('td.align_l > div > img')['src']
        team_name = tr.select_one('td.align_l > div > span').text
        played = tr.select_one('td:nth-child(3) > div > span').text
        points = tr.select_one('td.selected > div > span').text
        won = tr.select_one('td:nth-child(5) > div > span').text
        draw = tr.select_one('td:nth-child(6) > div > span').text
        lost = tr.select_one('td:nth-child(7) > div > span').text
        gf = tr.select_one('td:nth-child(8) > div > span').text
        ga = tr.select_one('td:nth-child(9) > div > span').text
        gd = tr.select_one('td:nth-child(10) > div > span').text

        emblem_b = emblem_a.split('=')
        emblem_c = emblem_b[1].split('&')
        emblem = emblem_c[0]

        epl_tables = {
            'rank': rank,
            'emblem': emblem,
            'team_name': team_name,
            'played': played,
            'points': points,
            'won': won,
            'draw': draw,
            'lost': lost,
            'gf': gf,
            'ga': ga,
            'gd': gd
        }
        db.epls.insert_one(epl_tables)


def insert_all():
    db.epls.drop()
    insert_tables()
    driver.quit()


insert_all()

# wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td.align_l > div > img (앰블렘)
# wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td.align_l > div > span (팀명)
# wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td:nth-child(3) > div > span (경기수)
# wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td.selected > div > span (승점)
# wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td:nth-child(5) > div > span (승)
# wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td:nth-child(6) > div > span (무)
# wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td:nth-child(7) > div > span (패)
# wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td:nth-child(8) > div > span (득)
# wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td:nth-child(9) > div > span (실)
# wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td:nth-child(10) > div > span
