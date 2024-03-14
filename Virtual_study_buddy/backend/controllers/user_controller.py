from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)
from flask_marshmallow import Marshmallow
from models import db, User, StudyPlan, StudyMaterial, StudySession, Reminder
from backend.schemas.user_schema import UserSchema
import werkzeug.security
from services.user_service import UserService, AuthenticationError, VerificationError, DatabaseError

app = Flask(__name__)
jwt = JWTManager(app)
ma = Marshmallow(app)

user_blueprint = Blueprint('user', __name__)

jwt.jwt_required_callback = jwt_required

@jwt.user_loader_callback_loader
def user_loader_callback(jwt_header, jwt_payload):
    username = jwt_payload['username']
    return User.query.filter_by(username=username).first()

@app.before_first_request
def create_tables():
    db.create_all()

@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = UserSchema().validate(data)
    if errors:
        return jsonify({'message': 'Invalid input data.', 'errors': errors}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    otp = data.get('otp')

    if not username or not email or not password or not otp:
        return jsonify({'message': 'Please provide all required fields.'}), 400

    try:
        hashed_password = werkzeug.security.generate_password_hash(password)
        existing_user = UserService.get_user_by_username(username)
        if existing_user:
            return jsonify({'message': 'User already exists.'}), 400
        user = UserService.register_user(username, email, hashed_password)
        UserService.verify_otp(user, otp)
        access_token = create_access_token(identity=user)
        return jsonify({'message': 'User registered successfully.', 'access_token': access_token}), 201
    except ValueError as ve:
        return jsonify({'message': 'Invalid value: ' + str(ve)}), 400
    except AuthenticationError as ae:
        return jsonify({'message': 'Authentication failed: ' + str(ae)}), 401
    except VerificationError as ve:
        return jsonify({'message': 'Verification failed: ' + str(ve)}), 403
    except DatabaseError as de:
        return jsonify({'message': 'Database error: ' + str(de)}), 500
    except Exception as e:
        return jsonify({'message': 'An error occurred. Please try again later.'}), 500


@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    otp = data.get('otp')

    if not email or not password or not otp:
        return jsonify({'message': 'Please provide all required fields.'}), 400

    try:
        user = UserService.authenticate_user(email, password)
        UserService.verify_otp(user, otp)
        access_token = create_access_token(identity=user)
        return jsonify({'message': 'Login successful.', 'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
