import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.epls


def get_urls():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://sports.news.naver.com/wfootball/index.nhn', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    ol = soup.select(' #content > div > div.home_feature > div.feature_side > div > ol> li')

    urls = []
    for li in ol:
        a = li.select_one('a')['href']
        if a is not None:
            base_url = "https://sports.news.naver.com"
            url = base_url + a
            urls.append(url)

    return urls


def get_articles(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('#content > div > div.content > div > div.news_headline > h4').text

    b = soup.select_one('#newsEndContents > span > img')
    if b is not None:
        img_url = soup.select_one('#newsEndContents > span > img')['src']
    else:
        img_url = soup.select_one('meta[property="og:image"]')['content']

    content = soup.select_one('#newsEndContents').text.strip()
    press = soup.select_one('#pressLogo > a > img')['src']
    post_date = soup.select_one('#content > div > div.content > div > div.news_headline > div > span').text
    print(url)
    doc = {
        'title': title,
        'img_url': img_url,
        'content': content[0:50] + '...',
        'press': press,
        'post_date': post_date,
        'article_url': url
    }
    db.newses.insert_one(doc)



def insert_news():
    db.newses.drop()
    urls = get_urls()
    for url in urls:
        get_articles(url)


insert_news()

# newsEndContents > span:nth-child(1) > img
# newsEndContents > table > tbody > tr > td > span > img
# newsEndContents > table > tbody > tr > td > span > img
# newsEndContents > div:nth-child(1) > span > img
