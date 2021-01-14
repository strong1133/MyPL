from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from tables import check_recent
from news import insert_news
from matches import schedules_insert_all

app = Flask('__name__')

client = MongoClient('localhost', 27017)
db = client.epls

# 최신화 체크-> selenium into MongoDB
check_recent()
insert_news()
schedules_insert_all()


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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

#######################################################################################################################
