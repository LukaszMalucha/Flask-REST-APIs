from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")  ## default port for mongo
db = client.BankAPI
users = db["Users"]


## Check for user existance
def UserExist(username):
	if users.find({"Username":username}).count()==0:
		return False
	else:
		return True


######################################################### Register

class Register(Resource):
	def	post(self):
		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]

		## check if user already exist
		if UserExist(username):
			retJson = {
				"status": 301,
				"msg": "Invalid Username"
			}
			return jsonify(retJson)

		## hashed password	
		hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())	

		## create user in mongodb
		users.insert({
				"Username": username,
				"Password": hashed_pw,
				"Own": 0,
				"Debt": 0
			})

		retJson = {
			"status": 200,
			"msg": "You successfully signed in"
		}

		return jsonify(retJson)		



################################################### Verify Password

def verifyPw(username, password):
	if not UserExist(username):
		return False

	## retrieve userpassword from db	
	hashed_pw = users.find({
		"Username":username
		})[0]["Password"]	

	## compare passwords
	if bcrypt.hashpw(password.encode('utf8'), hashed_pw)==hashed_pw:
		return True
	else:
		return False	

################################################### Check Cash & Debt

def cashWithUser(username):
	cash = users.find({
		"Username":username
		})[0]["Own"]
	return cash

def debtWithUser(username):
	debt = users.find({
		"Username": username
		})[0]["Debt"]		
	return debt

######################################### Generate Response Dictionary

def generateReturnDictionary(status,msg):
	retJson = {
		"status": status,
		"msg": msg
	}
	return retJson

#################################################### Verify Credentials

def verifyCredentials(username, password):
	if not UserExist(username):
		return generateReturnDictionary(301, "Invalid Username"), True  

	correct_pw = verifyPw(username, password)

	if not correct_pw:
		return generateReturnDictionary(302, "Incorrect Password"), True	
  
	return None, False	## false = no error, no dictionary


################################################ Update Account Details

def	updateAccount(username, balance):
	users.update({
			"Username": username
		},{
			"$set":{
				"Own": balance
			}
		})

def updateDebt(username, balance):
	users.update({
		"Username": username
		},{
			"$set":{
				"Debt": balance
			}
		})	


####################################################### REST CLASSES ########################################################






############################################################# Money Top-up

class Add(Resource):
	def post(self):
		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]
		money    = postedData["amount"]


		retJson, error = verifyCredentials(username, password)

		if error:
			return jsonify(retJson)

		if money<=0:
			return jsonify(generateReturnDictionary(304, "Amount must be >0"))	

		cash = cashWithUser(username)
		money-=1
		bank_cash = cashWithUser("BANK")
		## bank fee
		updateAccount("BANK", bank_cash+1)
		## update user account
		updateAccount(username, cash+money)	

		return jsonify(generateReturnDictionary(200, "Amount added successfully"))


############################################################# Money Transfer

class Transfer(Resource):
	def post(self):
		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]
		to       = postedData["to"]
		money    = postedData["amount"]

		retJson, error = verifyCredentials(username, password)

		if error:
			return jsonify(retJson)

		## check account balance	
		cash = cashWithUser(username)
		if cash<=0:
			return jsonify(generateReturnDictionary(304, "Your account balance is 0 or less"))	


		## person does not exist

		if not UserExist(to):
			return jsonify(generateReturnDictionary(301, "Receiver does not exist"))	


		cash_from = cashWithUser(username)
		cash_to   = cashWithUser(to)
		bank_cash = cashWithUser("BANK")

		updateAccount("BANK", bank_cash+1)
		updateAccount(to, cash_to + money - 1)
		updateAccount(username, cash_from - money)	

		return jsonify(generateReturnDictionary(200, "Amount Transfer successfull"))


############################################################# Money Balance

class Balance(Resource):
	def post(self):
		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]

		retJson, error = verifyCredentials(username, password)

		if error:
			return jsonify(retJson)

		## return user but without password and id 	
		retJson = users.find({
			"Username": username
		}, {
			"Password": 0,
			"_id": 0 
		})[0]

		return jsonify(retJson)	


############################################################# Take Loan

class TakeLoan(Resource):
	def post(self):
		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]
		money    = postedData["amount"]

		retJson, error = verifyCredentials(username, password)

		if error:
			return jsonify(retJson)


		cash = cashWithUser(username)
		debt = debtWithUser(username)
		updateAccount(username, cash+money)	
		updateDebt(username, debt + money)

		return jsonify(generateReturnDictionary(200, "Loan processed to your account"))


############################################################# Pay Loan

class PayLoan(Resource):
	def post(self):
		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]
		money    = postedData["amount"]

		retJson, error = verifyCredentials(username, password)

		if error:
			return jsonify(retJson)


		cash = cashWithUser(username)

		if cash < money:
			return jsonify(generateReturnDictionary(303, "Not Enough cash in your account"))

		debt = debtWithUser(username)

		updateAccount(username, cash - money)	
		updateDebt(username, debt - money)		

		return jsonify(generateReturnDictionary(200, "Loan balance was updated"))


api.add_resource(Register, '/register')
api.add_resource(Add, '/add')
api.add_resource(Transfer, '/transfer')
api.add_resource(Balance, '/balance')
api.add_resource(TakeLoan, '/takeloan')
api.add_resource(PayLoan, '/payloan')


# if __name__ == '__main__':
#     # Bind to PORT if defined, otherwise default to 5000.
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=False)     


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')



