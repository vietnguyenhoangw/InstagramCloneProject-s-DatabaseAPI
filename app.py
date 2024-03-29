# import class
from flask import Flask
from flask import Response
from flask import jsonify
from flask import g
from flask import request
from flask import make_response
import json
import sqlite3
import os

Image_FOLDER = os.path.join('static', 'image')

# data base name
DATABASE = 'database/instagram_db'

app = Flask(__name__, static_folder="image")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

''' GET DATA '''
# newfeeds table
@app.route('/newfeeds',methods=["GET"])
def newfeeds_list():
    db = get_db()
    data = db.execute('SELECT * FROM newfeeds WHERE status = "1" ').fetchall()
    res = []
    for newfeed in data:
        item = {
            'userID':newfeed[0],
            'userName':newfeed[1],
            'userProfileImage':newfeed[2],
            'PostImage':str(newfeed[3]),
            'Like':newfeed[4],
            'Caption':newfeed[5],
            'postTime':newfeed[6],
            'status':newfeed[7]
        }
        res.append(item)
    return jsonify({
        'newfeeds': res
    })

# newfeeds table
@app.route('/userposts',methods=["GET"])
def userposts_list():
    db = get_db()
    data = db.execute('SELECT * FROM newfeeds WHERE status = "2" ').fetchall()
    res = []
    for newfeed in data:
        item = {
            'userID':newfeed[0],
            'userName':newfeed[1],
            'userProfileImage':newfeed[2],
            'PostImage':str(newfeed[3]),
            'Like':newfeed[4],
            'Caption':newfeed[5],
            'postTime':newfeed[6],
            'status':newfeed[7]
        }
        res.append(item)
    return jsonify({
        'newfeeds': res
    })

# stories table
@app.route('/stories',methods=['GET'])
def stories_list():
	db = get_db()
	data = db.execute('SELECT * FROM stories WHERE status = "1"').fetchall()
	res = []
	for story in data:
		item = {
			'storyID':story[0],
			'userName':story[1],
			'userProfileImage':story[2],
			'storyImage':story[3],
			'status':story[4]
		}
		res.append(item)
	return jsonify({
		'stories': res
	})

# categories table
@app.route('/categories',methods=['GET'])
def categories_list():
	db = get_db()
	data = db.execute('SELECT * FROM categories WHERE status = "1"').fetchall()
	res = []
	for story in data:
		item = {
			'categoryID':story[0],
			'categoryName':story[1],
			'status':story[2]
		}
		res.append(item)
	return jsonify({
		'categories': res
	})

# notification
@app.route('/notification',methods=['GET'])
def notifications_list():
	db = get_db()
	data = db.execute('SELECT username, content, notifications.status from newfeeds inner join notifications on newfeeds.ID = notifications.UserID').fetchall()
	res = []
	for notification in data:
		item = {
			'UserName':notification[0],
			'Content':notification[1],
			'Status':notification[2]
		}
		res.append(item)
	return jsonify({
		'notifications': res
	})


# get test text 'hello world'
@app.route('/', methods=["GET"])
def hello():
    return "Hello World!"

# main method
# run at port 5000
if (__name__ == "__main__"):
	app.run(host='0.0.0.0',port=5000)

