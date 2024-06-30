from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['SECRET_KEY'] = '42769ccab55c0fbad66dbc1c5ee13de15c123db174bc731988acbccfac3d667d'
app.config["MONGO_URI"] = "mongodb://localhost:27017/filoDB"

# SetUp PyMongo
mongodb_client = PyMongo(app)
my_db = mongodb_client.db
collection = my_db['predict']


date_str = "1401/11/01 02:08:40"


query = {
    'createDatetime': {'$gt': date_str}
}

comments = collection.find(query).sort('createDatetime', 1)
dates = list(comments)

dates_dict = {}

for item in dates[::-1]:
    if item['createDatetime'][:10] in dates_dict:
        dates_dict[item['createDatetime'][:10]] += 1
    else:
        dates_dict[item['createDatetime'][:10]] = 1
    if len(dates_dict) > 29:
        break

keys_list = list(dates_dict.keys())
values_list = list(dates_dict.values())


@ app.route("/")
def sport_chart():
    return render_template('chart.html', labels=keys_list[::-1], values=values_list[::-1], title='Timeline')


if __name__ == "__main__":
    app.run(debug=True)
