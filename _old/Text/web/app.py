import os

from flask import Flask, jsonify, request
from flask_restful import Api, Resource

import bcrypt
import spacy

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)


client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]


def UserExists(username):
	if users.find({"Username":username}).count() == 0:
		return False
	else:
		return True	

def verifyPw(username, password):
	if not UserExists(username):
		return False

	hashed_pw = users.find({"username": username})[0]["password"]
	
	if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
		return True
	else:
		return False

def countTokens(username):
	tokens = users.find({"username": username})[0]["tokens"]
	return tokens


class Register(Resource):
	def post(self):
		postedData = request.get_json()

		username = posedData["username"]
		password = postedData["password"]

		if UserExists(username):
			retJson = {
				"status": 301,
				"msg": "Invalid Username"
			}
			return jsonify(retJson)

		hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
		
		users.insert_one({
			"username": username,
			"password": hashed_pw,
			"tokens": 10
			})	

		retJson = {
			"status": 200,
			"msg": "Sign up successfull"
		}
		return jsonify(retJson)


class Detect(Resource):
	def post(self):
		postedData = request.get_json()

		username = psotedData["username"]
		password = postedData["password"]
		text1 = postedData["text1"]
		text2 = posedData["text2"]

		if not USerExists(username):
			retJson = {
				"status": "301",
				"msg": "Invalid Username"
			}		
			return jsonify(retJson)


		correct_pw = verifyPw(username, password)	


		if not correct_pw:
			retJson = {

				"status": 302,
				"msg": "Invalid Password"
			}
			return jsonify(retJson)

		num_tokens = countTokens(username)

		if num_tokens <= 0:
			retJson = {
				"status": 303,
				"msg": "No tokens left"
			} 	
			return jsonify(retJson) 

### LOAD SPACY NLP MODEL

		nlp = spacy.load('en_core_web_sm')

		text1 = nlp(text1)
		text2 = nlp(text2)

### SIMILARITY RATIO
		ratio = text1.similarity(text2)

		retJson = {
			"status": 200,
			"similarity": ratio,
		}	

		current_tokens = countTokens(username)

		users.update({"username": username}, {"$set":{"tokens": current_tokens-1}})

		return jsonify(retJson)


class Refill(Resource):
	def post(self):
		postedData = request.get_json()

		username = postedData["username"]
		password = posedData["admin_pw"]
		refill_amount = postedData["refill"]		

		if not UserExists(username):
			retJson = {
				"status": 301,
				"msg": "Invalid Username"
			}
			return jsonify(retJson)

		## hard coded, not hashed for testing only	
		admin_pw = "password"	
		if not password == admin_pw:
			retJson = {
				"status": 304,
				"msg": "invalid admin password"
			}
			return jsonify(retJson)

		current_tokens = countTokens(username)
		users.update({"username":username}, {"$set":{"tokens": refill_amount+current_tokens}})	

		retJson = {
			"status": 200,
			"msg": "Refilled Successfully"
		}	
		return jsonify(retJson)


api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')


if "__name__" == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
	
