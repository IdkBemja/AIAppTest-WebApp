from app.utils.mysqlconnection import connectToMySQL
from app.utils.config.env_config import get_db
import jwt
import datetime
from app.utils.config.env_config import get_secret_key

database = get_db()['dbname']

def generate_jwt(data_list, expires_in_minutes=60):
	payload = {
		'data': data_list,
		'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_in_minutes)
	}
	token = jwt.encode(payload, get_secret_key(), algorithm='HS256')
	if isinstance(token, bytes):
		token = token.decode('utf-8')
	return token

def decode_jwt(token):
	try:
		payload = jwt.decode(token, get_secret_key(), algorithms=['HS256'])
		return payload.get('data', [])
	except jwt.ExpiredSignatureError:
		raise ValueError('Token has expired')
	except jwt.InvalidTokenError:
		raise ValueError('Invalid token')

def add_token_to_blacklist(token):
	query = "INSERT INTO jwt_blacklist (token) VALUES (%(token)s);"
	data = {'token': token}
	connectToMySQL(database).query_db(query, data)

def is_token_blacklisted(token):
	query = "SELECT id FROM jwt_blacklist WHERE token = %(token)s;"
	data = {'token': token}
	result = connectToMySQL(database).query_db(query, data)
	return bool(result)
