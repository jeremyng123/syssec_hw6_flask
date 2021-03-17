from flask import Flask, request, jsonify
from flask_cors import CORS
from mymongo import *
from random import randint, seed, shuffle
import json
import re
# from flask_pymongo import PyMongo

file = open('words_dictionary.json', 'r')
words = json.load(file).keys()
file.close()

app = Flask(__name__)

# app.config['MONGO_DBNAME'] = 'syssec_hw6'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/'+app.config['MONGO_DBNAME']

# mongo = PyMongo(app)
mongo = getMongoDBClient()


@app.route('/')
def home():
    return "System Sec hw6"


@app.route('/register', methods=['POST'])
def register():
    users = getMongoDBCollection(mongo, 'users')
    username = request.json['username']
    password = request.json['password']
    tail = request.json['tail']
    t = request.json['t']
    method = request.json['genPasswordType']
    userid = ObjectId()
    passwords = chaffing(method, userid, password, tail, t)
    schema = {'_id': userid, 'username': username}
    schema.update(passwords)
    user_id = users.insert_one(schema)
    print(schema)
    return jsonify({'_id': str(user_id.inserted_id)})


@app.route('/login', methods=['POST'])
def login():
    users = getMongoDBCollection(mongo, 'users')
    username = request.json['username']
    password = request.json['password']
    user = users.find_one({'username': username})
    if user is None:
        return 'failed'
    # print(user)
    seed(str(user['_id']))
    true_index = randint(0, K)
    passwords = [user['password' + str(index)] for index in range(0, K)]
    if password in passwords:
        return 'sugarword' if passwords.index(
            password) == true_index else 'honeyword'
    return 'failed'


def chaffing(method, userid, password, tail, t):
    seed(str(userid))
    true_index = randint(0, K)
    print(f"true_index: {true_index}")
    answer = {}
    for i in range(0, K):
        answer["password" + str(i)] = 0
    if method == 'chaffing-by-tweaking':
        """
        This method will assume tail-tweaking along the password. 
        """
        for i in range(0, len(answer)):
            answer["password" + str(i)] = password + tweak_digit(
                t) if i != true_index else password + tail
        return answer
    elif method == 'chaffing-with-a-password-model':
        """
        Assume that the password is separated by password (alpha) and tail (numeric)
        """
        honeywords = replaceWord(password)
        for i in range(len(answer)):
            answer["password" + str(i)] = honeywords[
                i] + tail if i != true_index else password + tail
        return answer

    elif method == 'hybrid':
        """
        Combines both replace word and tweaking of digits
        """
        honeywords = replaceWord(password)
        for i in range(len(answer)):
            answer["password" + str(i)] = honeywords[i] + tweak_digit(
                t) if i != true_index else password + tail
        return answer
    else:
        print(f"expected 'chaffing-by-tweaking' \
      or 'chaffing-with-a-password-model' \
      or 'hybrid' method \
      but instead, got {method}")


def tweak_digit(t):
    return str(randint(0, int("9" * t) + 1)).zfill(t)


def replaceWord(password):
    length = len(password)
    keyword = [word for word in words if len(word) == length]
    shuffle(keyword)
    count = 0
    toreturn = []
    for word in keyword:
        toreturn.append(word)
        count += 1
        if count >= K:
            break
    return toreturn


if __name__ == '__main__':
    CORS(app)
    app.run(debug=True)
