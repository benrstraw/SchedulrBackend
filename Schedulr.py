import schedulr_config
from flask import Flask, request, abort, session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import sqlalchemy as db
import json
import bcrypt
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
app.config.from_object(schedulr_config.Config)
jwt = JWTManager(app)
engine = db.create_engine(schedulr_config.Config.DATABASE_URI)
connection = engine.connect()
metadata = db.MetaData()
classes = db.Table('classes', metadata, autoload=True, autoload_with=engine)
class_reqs = db.Table('class_reqs', metadata, autoload=True, autoload_with=engine)
classes_taken = db.Table('classes_taken', metadata, autoload=True, autoload_with=engine)
programs = db.Table('programs', metadata, autoload=True, autoload_with=engine)
prog_reqs = db.Table('prog_reqs', metadata, autoload=True, autoload_with=engine)
reqsets = db.Table('reqsets', metadata, autoload=True, autoload_with=engine)
requirements = db.Table('requirements', metadata, autoload=True, autoload_with=engine)
users = db.Table('users', metadata, autoload=True, autoload_with=engine)
user_reqs = db.Table('user_reqs', metadata, autoload=True, autoload_with=engine)

@app.route("/auth", methods=['POST'])
@jwt_required
def auth():
	return {
		"error": "success",
		"user_id": get_jwt_identity()
	}, 200

@app.route("/login", methods=['POST'])
def login():
	if not request.is_json:
		return { "error": "Invalid JSON request!" }, 400

	email = request.json.get('email')
	password = request.json.get('password')

	if not email:
		return { "error": "no email" }, 400
	if not password:
		return { "error": "no password" }, 400

	query = db.select([users]).where(users.columns.email == email)
	ResultProxy = connection.execute(query)
	result = ResultProxy.first()
	if not result or not bcrypt.checkpw(password.encode('utf-8'), result['password'].encode('utf-8')):
		return { "error": "bad login" }, 401

	access_token = create_access_token(identity=result['user_id'])

	return {
		"error": "success",
		"access_token": access_token
	}

@app.route("/signup", methods=['POST'])
def signup():
	if not request.is_json:
		return { "error": "Invalid JSON request!" }, 400

	email = request.json.get('email')
	password = request.json.get('password')
	name = request.json.get('name')

	if not email:
		return { "error": "no email" }, 400
	if not password:
		return { "error": "no password" }, 400
	if not name:
		return { "error": "no name" }, 400

	try:
		v = validate_email(email, check_deliverability=False)
		email = v['email']
	except EmailNotValidError as e:
		return { "error": "invalid email" }, 400

	query = db.select([users]).where(users.columns.email == email)
	ResultProxy = connection.execute(query)
	result = ResultProxy.first()
	if result:
		return { "error": "email exists" }, 409

	hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

	query = users.insert().values(email=email, password=hashed, name=name)
	ResultProxy = connection.execute(query)

	user_id = ResultProxy.inserted_primary_key[0]

	access_token = create_access_token(identity=user_id)

	return {
		"error": "success",
		"access_token": access_token
	}

app.run()