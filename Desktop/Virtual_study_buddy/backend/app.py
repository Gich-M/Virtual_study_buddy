from flask import Flask, Blueprint,  jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from models.user_model import User
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

user_blueprint = Blueprint('user', __name__)
resource_blueprint = Blueprint('resource', __name__)
study_plan_blueprint = Blueprint('study_plan', __name__)

app.register_blueprint(study_plan_blueprint, url_prefix='/study_plan')
app.register_blueprint(resource_blueprint, url_prefix='/resources')
app.register_blueprint(user_blueprint, url_prefix='/user')

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not username or not email or not password:
        return jsonify({'message': 'Please provide all required fields.'}), 400
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'message': 'Email already in use.'}), 400
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        user.save()
        access_token = create_access_token(identity=user.email)
        return jsonify({'message': 'User registered successfully.', 'access_token': access_token}), 201
    except IntegrityError:
        return jsonify({'message': 'Username or email already exists.'}), 400

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
    return jsonify({'message': 'Authentication successful.', 'access_token': access_token}), 200

if __name__ == '__main__':
    app.run(debug=True)
