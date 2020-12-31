from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask('__name__')

client = MongoClient('localhost', 27017)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/borders', methods=['GET'])
def get_borders():
    epls = list(db.epls.find({}, {'_id': 0}))
    print(epls)
    return jsonify({'result': 'success', 'epls': epls})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
