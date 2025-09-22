
from app.utils.mysqlconnection import connectToMySQL
from app.utils.config.env_config import get_db
from jwt import ExpiredSignatureError, InvalidTokenError
from app.utils.jwt import decode_jwt

database = get_db()['dbname']


class User:

    def __init__(self, data):

        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.token = data['token']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (username, password, token) VALUES (%(username)s, %(password)s, %(token)s);"
        return connectToMySQL(database).query_db(query, data)

    @classmethod
    def get_by_username(cls, username):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        data = {'username': username}
        result = connectToMySQL(database).query_db(query, data)
        if result:
            return cls(result[0])
        return None
    
    @staticmethod
    def validate_user(form):
        is_valid = True
        errors = []
        if len(form['username']) < 3:
            errors.append("Username must be at least 3 characters.")
            is_valid = False

        if len(form['password']) < 6:
            errors.append("Password must be at least 6 characters.")
            is_valid = False

        if ' ' in form['username'] or ' ' in form['password'] or ' ' in form['token']:
            errors.append("No spaces allowed in username, password, or token.")
            is_valid = False
            
        if len(form['token']) < 10:
            errors.append("Token must be at least 10 characters.")
            is_valid = False

        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL(database).query_db(query, form)
        if len(results) >= 1:
            is_valid = False
            errors.append("Username already exists.")
            
        return {'is_valid': is_valid, 'errors': errors}
    

    @staticmethod
    def verify_identity(auth_header):
        """
        Verifies the Authorization header, decodes the JWT, checks expiration, and matches user/token.
        Returns (user, error_message) tuple. If user is valid, error_message is None.
        """
        if not auth_header:
            return None, 'Authorization header is missing.'
        try:
            token = auth_header.split(" ")[1]
            decoded_data = decode_jwt(token)
            if len(decoded_data) != 2:
                return None, 'Invalid token data.'
            username, user_token = decoded_data
        except ExpiredSignatureError:
            return None, 'Token has expired.'
        except (IndexError, InvalidTokenError, ValueError):
            return None, 'Invalid or malformed token.'

        user = User.get_by_username(username)
        if not user or user.token != user_token:
            return None, 'Invalid token or user not found.'
        return user, None

