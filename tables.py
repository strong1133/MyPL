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
        db.tables.insert_one(epl_tables)


def insert_all():
    db.tables.drop()
    insert_tables()
    driver.quit()


def check_recent():
    trs = soup.select('#wfootballTeamRecordBody > table > tbody > tr')
    sum_selenium = 0
    for tr in trs:
        played = tr.select_one('td:nth-child(3) > div > span').text
        type_int = int(played)
        sum_selenium += type_int

    finds = list(db.tables.find({}, {'_id': 0, 'played': 1}))

    sum_db = 0
    for find in finds:
        c = find['played']
        s = int(c) + 0
        sum_db += s

    print(sum_selenium, sum_db)
    if sum_selenium == sum_db:
        print('최신 상태입니다.')
        driver.quit()
    else:
        print('최신화가 필요합니다.')
        insert_all()
        driver.quit()
