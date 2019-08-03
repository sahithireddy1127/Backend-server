import time
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, jsonify
import datetime
import requests
import json

import os
from redis_connector import *
from db_connector import * 
app = Flask(__name__)
app.config['DEBUG'] = True

# This method validates the input. checks for value and size.

def validation ( frm , to, msg ):

	if frm=="":
		return jsonify({"message": "", "error": "from is missing"}) 
	elif to =="":
	    return jsonify({"message": "", "error": "to is missing"})
	elif msg=="":
	    return jsonify({"message": "", "error": "text is missing"})
	elif not 6<=len(frm)<=16:
	    return jsonify({"message": "", "error": frm+" is invalid"})
	elif not 6<=len(to)<=16:
	    return jsonify({"message": "", "error": to+" is invalid"})
	elif not 1<=len(msg)<=120:
	    return jsonify({"message": "", "error": msg+" is invalid"})
	else:
	    return "valid"

#This method stores the phone number and the count of number of API requests made by the from number. 
#It returns false if it exceeds the limit within 24 hrs. else true

def apiRequestLimitCheck(phno):
	num = getFromCache(phno+"count")
	if num == None:
		# if the number is not present in cache, it adds the number to cache with count = 1, expire as 24 hrs
		setToCache(phno+"count",1,24, True)
	elif num.decode('utf-8') == 50:
		# if number exceeds 50, returns false
		return False	
	else:
		# If number is already in cache and limit not exceeded. It updates the cache by incrementing count and does not set any expire time.
		print(int(num.decode('utf-8')))
		num = int(num.decode('utf-8'))
		num+=1
		setToCache(phno+"count",num,0, False)
	return True


@app.route('/inbound/sms', methods= ['POST'])
def inbound():
	try:
		#if method is not post returns HTTP 405
		if request.method !='POST':
			return render_template('errorStatusCode.html', status=405)
		#fetches the userId and password from json
		details = request.get_json()
		userId = details['authentication']['username']
		authId = details['authentication']['password']
		# authenticates the user by checking from DB
		if(authentication(userId,authId)):
			to_num = details['to']
			from_num = details['from']
			msg = details['text']
			#validates the input parameters
			validationStatus = validation(from_num,to_num,msg);
			if(validationStatus == "valid" ):
				#checks if the phone number is associated with the user. 
				if(validateParameters(to_num , userId)):
					#checks if the from has not reached the limit of 50 requests with in 24 hrs
					if(apiRequestLimitCheck(from_num)):
						# If message has stop then it sends to the cache. with 4hrs as time limit
						if msg in ('STOP', 'STOP\n', 'STOP\r', 'STOP\r\n'):

							setToCache(to_num,from_num, 4, True)	
						return jsonify({"message": "inbound sms ok", "error": "" })
					else:
						return jsonify({"message": "", "error": "limit reached for from "+from_num +""})
				else:
					return jsonify({"message": "", "error": "to parameter not found" })
			else:
				return validationStatus
		else:
			return render_template('errorStatusCode.html', status=403)
	except:
		return jsonify({"message": "", "error": "unknown failure" })



@app.route('/outbound/sms', methods= ['POST'])
def outbound():
	try:
		#if method is not post returns HTTP 405
		if request.method !='POST':
			return render_template('errorStatusCode.html', status=405)
		#fetches the userId and password from json
		details = request.get_json()
		userId = details['authentication']['username']
		authId = details['authentication']['password']
		# authenticates the user by checking from DB
		if(authentication(userId,authId)):
			to_num = details['to']
			from_num = details['from']
			msg = details['text']
			#validates the input parameters
			validationStatus = validation(from_num,to_num,msg);
			if(validationStatus == "valid" ):
				#checks if the phone number is associated with the user. 
				if(validateParameters(from_num , userId)):
					#checks the from has not reached the limit of 50 requests with in 24 hrs
					if(apiRequestLimitCheck(from_num)):
						# checks if the number was blocked.
						if isBlocked(to_num,from_num):
							return jsonify({"message": "", "error": "sms from "+ from_num +"to "+to_num+" blocked by STOP request"})
						else:
							return jsonify({"message": "outbound sms ok", "error": "" })
					else:
						return jsonify({"message": "", "error": "limit reached for from "+from_num +""})
				else:
					return jsonify({"message": "", "error": "from parameter not found" })
			else:
				return validationStatus
		else:
			return render_template('errorStatusCode.html', status=403)
	except (Exception) as e:
		return jsonify({"message": "", "error": "unknown failure" })

if __name__ =='__main__':
	app.run(debug=True)
