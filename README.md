# Backend-server
A micro service API server that exposes the following 2 APIs that accept JSON data as input to POST requests. 

### API Behaviour For Inbound
-  Authentication is based on username and auth_id
-  Input validation 
-  ‘to’ parameter check in phone_number table for this specific account 
-  The ‘from’ and ‘to’  pair is stored in cache as a unique entry and expire's after 4 hours

### API Behaviour For Outbound
-  Authentication is based on username and auth_id
-  Input validation 
-  ‘from’ parameter check in phone_number table for this specific account 
-  Using cache, does not allow more then 50 API requests for a number in 24 hrs.
-  If the pair ‘to’, ‘from’ matches any entry in cache (STOP) returns error 


##  Instructions to setup
- python- 3.7
- Postgres 
- Postman
- Redis

## Installations
- flask
- mock
- redis
- psycopg2

## Steps to run the code in local

- First create a database in postgres sql shell CLI.
- Dump the schema.sql into the database using the command "\i schema.sql".
- Run Redis server
- Run pip install -r requirements.txt in the command prompt
- Update the database details with your details in code
- Run py flask_app.py

## Testing using Postman
- Open postman and set method as "POST" and "url" as "http://127.0.0.1:5000/inbound/sms"
- In 'Body'  select 'raw' and keep type as JSON type
- This is the sample JSON request

{"authentication": 
{"username": "azr3","password": "9LLV6I4ZWI"},
"from": "441235330053",
"to": "441224980093",
"text": "STOP"
}
- Hit send and check for response.

## Unit Testing
- Run  py test_flask_app.py 
- you can see the response code for both the API's

    

