# Backend-server
A micro service API server that exposes the following 2 APIs that accept JSON data as input to POST requests. 

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

    

