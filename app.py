
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from tables import check_recent
from news import insert_news
from matches import schedules_insert_all
from lead_player import insert_leaders

app = Flask('__name__')

client = MongoClient('mongodb://tjrwls455:3879@13.125.246.107', 27017)
db = client.epls


# 최신화 체크-> selenium into MongoDB
def recently():
    print("===최신화===")
    check_recent()
    insert_news()
    schedules_insert_all()
    insert_leaders()


# 최초 실행시 최신화 체크
check_recent()

# 주기적으로 최신화 반복
sched = BackgroundScheduler()
sched.start()
sched.add_job(recently, 'interval', seconds=120, id="test_2")


#######################################################################################################################

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/tables', methods=['GET'])
def get_tables():
    tables = list(db.tables.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'tables': tables})


@app.route('/api/news', methods=['GET'])
def get_news():
    newses = list(db.newses.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'newses': newses})


@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    schedules = list(db.schedules.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'schedules': schedules})


@app.route('/api/leaders', methods=['GET'])
def get_leaders():
    leaders = list(db.lead_player.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'leaders': leaders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

#######################################################################################################################
