import psycopg2
from psycopg2 import Error

# Establishes DB connection and fetchs the data from the Db.
def postgresSqlConnector(query):
	status = False
	try:
		connection = psycopg2.connect(user = "postgres",
		                              password = "sahithi",
		                              host = "127.0.0.1",
		                              port = "5432",
		                              database = "auzmorassignment")
		cursor = connection.cursor()
		cursor.execute(query)
		accounts = cursor.fetchall()
		# checks if the account is present
		if(len(accounts) == 1):
			status = True		
		print(accounts)
		connection.commit()
		cursor.close()
		connection.close()
		print(status)
		return status

	except (Exception, psycopg2.DatabaseError) as error :
		if(connection):
			cursor.close()
			connection.close()
		print ("Error while accessing PostgreSQL table", error)
		raise Exception('Error while accessing PostgreSQL table')
	
# This method builds the query and performs authentication
def authentication (username, password ):
	authenticationQuery = " SELECT * FROM account where username = '"+ username+"' and  auth_id = '"+password+"';"
	return postgresSqlConnector(authenticationQuery)
	
# This method builds the query and validate the phone number with auth_id
def validateParameters(num, authId):
	validateParameterQuery = " SELECT * FROM phone_number where number = '"+ num+"' and  account_id in (select id from account where username = '"+authId+"');"
	return postgresSqlConnector(validateParameterQuery)
