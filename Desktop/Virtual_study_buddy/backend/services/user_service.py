import bcrypt
from validators import validate_email
from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)
from models.user_model import User
from sqlalchemy.exc import IntegrityError
import os
import random
import string
import pyotp
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    """
    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    if not username or not email or not password:
        return jsonify({'message': 'Please provide all required fields.'}), 400
    
    if not validate_email(email):
        return jsonify({'message': 'Invalid email address.'}), 400
    
    if not username.isalnum() or '_' not in username or len(username) < 3 or len(username) > 50:
        return jsonify({'message': 'Invalid username.'}), 400
    
    if len(password) < 8 or not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char.isdigit() for char in password) or not any(char in string.punctuation for char in password):
        return jsonify({'message': 'Password must be at least 8 characters long and contain a mix of uppercase and lowercase letters, numbers, and special characters.'}), 400
    
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'message': 'Email already in use.'}), 400
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(username=username, email=email, password=hashed_password)
        user.save()
        
        access_token = create_access_token(identity=user.email)
        return jsonify({'message': 'User registered successfully.', 'access_token': access_token}), 201
    
    except IntegrityError:
        return jsonify({'message': 'Username or email already exists.'}), 400
    
    except Exception as e:
        return jsonify({'message': 'An error occurred.', 'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email or not password:
        return jsonify({'message': 'Please provide all required fields.'}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password.'}), 401
    access_token = create_access_token(identity=user.email)
    session['user_id'] = user.user_id
    return jsonify({'message': 'Authentication successful.', 'access_token': access_token}), 200

@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.json.get('email', None)
    if not email:
        return jsonify({'message': 'Please provide an email address.'}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'No user found with that email address.'}), 404
    new_password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
    user.password = bcrypt.generate_password_hash(new_password)
    user.save()
    return jsonify({'message': 'Password reset successfully.', 'new_password': new_password}), 200

@app.route('/verify-email', methods=['POST'])
@jwt_required
def verify_email():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    user.email_verified = True
    user.save()
    return jsonify({'message': 'Email verified successfully.'}), 200

@app.route('/update-password', methods=['POST'])
@jwt_required
def update_password():
    current_password = request.json.get('current_password', None)
    new_password = request.json.get('new_password', None)
    if not current_password or not new_password:
        return jsonify({'message': 'Please provide all required fields.'}), 400
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user or not bcrypt.check_password_hash(user.password, current_password):
        return jsonify({'message': 'Invalid current password.'}), 401
    user.password = bcrypt.generate_password_hash(new_password)
    user.save()
    return jsonify({'message': 'Password updated successfully.'}), 200

@app.route('/users', methods=['GET'])
@jwt_required
def get_users():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    users = User.query.all()
    return jsonify({'message': 'Users retrieved successfully.', 'users': [user.to_dict() for user in users]}), 200

@app.route('/users/<int:user_id>', methods=['GET'])
@jwt_required
def get_user(user_id):
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    user = User.query.get_or_404(user_id)
    return jsonify({'message': 'User retrieved successfully.', 'user': user.to_dict()}), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required
def update_user(user_id):
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    user_to_update = User.query.get_or_404(user_id)
    if user_to_update.email != user.email:
        return jsonify({'message': 'You do not have permission to update this user.'}), 403
    data = request.get_json()
    for key, value in data.items():
        setattr(user_to_update, key, value)
    user_to_update.save()
    return jsonify({'message': 'User updated successfully.', 'user': user_to_update.to_dict()}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required
def delete_user(user_id):
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    user_to_delete = User.query.get_or_404(user_id)
    if user_to_delete.email != user.email:
        return jsonify({'message': 'You do not have permission to delete this user.'}), 403
    user_to_delete.delete()
    return jsonify({'message': 'User deleted successfully.'}), 200

@app.route('/generate-reset-token', methods=['POST'])
def generate_reset_token():
    email = request.json.get('email', None)
    if not email:
        return jsonify({'message': 'Please provide an email address.'}), 400
    serializer = URLSafeTimedSerializer(app.config['JWT_SECRET_KEY'])
    reset_token = serializer.dumps(email, salt=app.config['JWT_SECRET_SALT'])
    return jsonify({'reset_token': reset_token}), 200

@app.route('/verify-reset-token', methods=['POST'])
def verify_reset_token():
    reset_token = request.json.get('reset_token', None)
    if not reset_token:
        return jsonify({'message': 'Please provide a reset token.'}), 400
    serializer = URLSafeTimedSerializer(app.config['JWT_SECRET_KEY'])
    try:
        email = serializer.loads(
            reset_token,
            salt=app.config['JWT_SECRET_SALT']
        )
    except:
        return jsonify({'message': 'Invalid reset token.'}), 400
    return jsonify({'email': email}), 200

@app.route('/generate-confirmation-token', methods=['POST'])
def generate_confirmation_token():
    email = request.json.get('email', None)
    if not email:
        return jsonify({'message': 'Please provide an email address.'}), 400
    serializer = URLSafeTimedSerializer(app.config['JWT_SECRET_KEY'])
    confirmation_token = serializer.dumps(email, salt=app.config['JWT_SECRET_SALT'])
    return jsonify({'confirmation_token': confirmation_token}), 200

@app.route('/confirm-token', methods=['POST'])
def confirm_token():
    confirmation_token = request.json.get('confirmation_token', None)
    if not confirmation_token:
        return jsonify({'message': 'Please provide a confirmation token.'}), 400
    serializer = URLSafeTimedSerializer(app.config['JWT_SECRET_KEY'])
    try:
        email = serializer.loads(
            confirmation_token,
            salt=app.config['JWT_SECRET_SALT']
        )
    except:
        return jsonify({'message': 'Invalid confirmation token.'}), 400
    return jsonify({'email': email}), 200

@app.route('/generate-otp', methods=['POST'])
@jwt_required
def generate_otp():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    user.enable_otp()
    return jsonify({'message': 'OTP enabled successfully.'}), 200

@app.route('/verify-otp', methods=['POST'])
@jwt_required
def verify_otp():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    otp = request.json.get('otp', None)
    if not otp:
        return jsonify({'message': 'Please provide an OTP.'}), 400
    if user.verify_otp(otp):
        return jsonify({'message': 'OTP verified successfully.'}), 200
    else:
        return jsonify({'message': 'Invalid OTP.'}), 401

if __name__ == '__main__':
    app.run(debug=True)
