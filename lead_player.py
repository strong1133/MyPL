import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb://tjrwls455:3879@13.125.246.107', 27017)
db = client.epls

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://sports.news.naver.com/wfootball/record/index.nhn?category=epl&year=2020&tab=player',
                    headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')


def get_leaders():
    ul = soup.select('#content > div.record_lead > ul > li')
    for li in ul:
        divs = li.select(' div > div.list > div')
        player_img = li.select_one('div > div.image > img')
        for div in divs:
            name = div.select_one('div.info > span.name').text
            team = div.select_one('div.info > span.team').text
            stat = div.select_one('div.stat').text.strip()

            doc = {
                'name': name,
                'team': team,
                'stat': stat,
                'player_img': player_img['src']
            }
            db.lead_player.insert_one(doc)

def insert_leaders():
    db.lead_player.drop()
    get_leaders()

# content > div.record_lead > ul > li:nth-child(1) > div > div.list > div.text.best > div.info > span.name
# content > div.record_lead > ul > li:nth-child(1) > div > div.list > div:nth-child(2) > div.info > span.name
# content > div.record_lead > ul > li:nth-child(1) > div > div.list > div:nth-child(3) > div.info > span.name
# content > div.record_lead > ul > li:nth-child(1) > div > div.list > div.text.best > div.stat

# content > div.record_lead > ul > li:nth-child(1) > div > div.image > img
