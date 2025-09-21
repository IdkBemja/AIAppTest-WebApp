from app.utils.jwt import add_token_to_blacklist, is_token_blacklisted
from Flask import request, jsonify
from app import app
from app.models import User
from flask_bcrypt import Bcrypt
from app.utils.jwt import generate_jwt, decode_jwt
from app.utils.OpenAIUtil import ask_openai
bcrypt = Bcrypt(app)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    validation = User.validate_user(data)

    if not validation['is_valid']:
        return jsonify({'error': validation['errors']}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    data['password'] = hashed_password
    User.save(data)

    return jsonify({'success': 'User registered successfully.'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.get_by_username(username)
    if not user:
        return jsonify({'error': 'Invalid username or password.'}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password.'}), 401

    jwt_data = generate_jwt([user.username, user.token])

    return jsonify({'token': jwt_data}), 200

@app.route('/api/ask', methods=['POST'])
def ask():
    auth_header = request.headers.get('Authorization')
    try:
        token = auth_header.split(" ")[1]
    except Exception:
        return jsonify({'error': 'Malformed Authorization header.'}), 400
    if is_token_blacklisted(token):
        return jsonify({'error': 'Token is blacklisted.'}), 401
    user, error = User.verify_identity(auth_header)
    if error:
        return jsonify({'error': error}), 401

    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'Question is required.'}), 400

    ia_token = user.token
    try:
        response = ask_openai(question, system_prompt="You are a helpful assistant.", api_key=ia_token)
    except Exception as e:
        return jsonify({'error': f'OpenAI error: {str(e)}'}), 500

    return jsonify({'response': response}), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Authorization header is missing.'}), 401
    try:
        token = auth_header.split(" ")[1]
    except Exception:
        return jsonify({'error': 'Malformed Authorization header.'}), 400
    add_token_to_blacklist(token)
    return jsonify({'success': 'Logged out and token blacklisted.'}), 200

@app.route('/api/refresh-token', methods=['POST'])
def refresh_token():
    auth_header = request.headers.get('Authorization')
    user, error = User.verify_identity(auth_header)
    if error:
        return jsonify({'error': error}), 401

    new_jwt = generate_jwt([user.username, user.token])
    return jsonify({'token': new_jwt}), 200