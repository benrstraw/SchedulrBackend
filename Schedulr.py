import schedulr_config
from flask import Flask, request, abort, session, jsonify
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
courses = db.Table('courses', metadata, autoload=True, autoload_with=engine)
course_reqs = db.Table('course_reqs', metadata, autoload=True, autoload_with=engine)
courses_taken = db.Table('courses_taken', metadata, autoload=True, autoload_with=engine)
programs = db.Table('programs', metadata, autoload=True, autoload_with=engine)
prog_reqs = db.Table('prog_reqs', metadata, autoload=True, autoload_with=engine)
reqsets = db.Table('reqsets', metadata, autoload=True, autoload_with=engine)
requirements = db.Table('requirements', metadata, autoload=True, autoload_with=engine)
users = db.Table('users', metadata, autoload=True, autoload_with=engine)
user_reqs = db.Table('user_reqs', metadata, autoload=True, autoload_with=engine)

@app.route("/list_courses", methods=['GET'])
def list_courses():
	sel = db.select([courses])
	res = connection.execute(sel)
	db_out = res.fetchall()
	res.close()
	return jsonify([(dict(row.items())) for row in db_out]), 200

@app.route("/list_programs", methods=['GET'])
def list_programs():
	sel = db.select([programs])
	res = connection.execute(sel)
	db_out = res.fetchall()
	res.close()
	return jsonify([(dict(row.items())) for row in db_out]), 200

@app.route("/get_course", methods=['GET'])
def get_course():
	cid = request.args.get('course_id')
	if not cid:
		return { "error": "no course_id" }, 400

	sel = db.select([courses]).where(courses.c.course_id == cid)
	res = connection.execute(sel)
	db_out = res.first()

	if not db_out:
		return { "error": "invalid course" }, 404

	course_info = dict(db_out.items())

	sel = db.select([courses]).select_from(courses.join(course_reqs, courses.c.course_id == course_reqs.c.prereq_id)).where(course_reqs.c.course_id == cid)
	res = connection.execute(sel)
	db_out = res.fetchall()

	course_info['prereqs'] = [(dict(row.items())) for row in db_out]

	res.close()

	return course_info, 200

@app.route("/list_taken", methods=['GET', 'POST'])
@jwt_required
def list_taken():
	uid = get_jwt_identity()
	sel = db.select([courses_taken]).where(courses_taken.c.user_id == uid)
	res = connection.execute(sel)
	db_out = res.fetchall()

	takens = [(dict(row.items())) for row in db_out]

	for t in takens:
		sel = db.select([courses]).where(courses.c.course_id == t['course_id'])
		res = connection.execute(sel)
		db_out = res.first()
		t['course'] = dict(db_out.items())

	res.close()
	return jsonify(takens), 200

@app.route("/add_taken", methods=['POST'])
@jwt_required
def add_taken():
	if not request.is_json:
		return { "error": "invalid JSON" }, 400

	cid = request.json.get('course_id')
	grade = request.json.get('grade')
	status = request.json.get('status')

	if not cid:
		return { "error": "no email" }, 400
	if not status:
		return { "error": "no name" }, 400

	query = courses_taken.insert().values(user_id=get_jwt_identity(), course_id=cid, grade=grade, status=status)
	ResultProxy = connection.execute(query)

	return {
		"taken_id": ResultProxy.inserted_primary_key[0]
	}, 200

@app.route("/auth", methods=['GET'])
@jwt_required
def auth():
	return {
		"user_id": get_jwt_identity()
	}, 200

@app.route("/login", methods=['POST'])
def login():
	if not request.is_json:
		return { "error": "invalid JSON" }, 400

	email = request.json.get('email')
	password = request.json.get('password')

	if not email:
		return { "error": "no email" }, 400
	if not password:
		return { "error": "no password" }, 400

	query = db.select([users]).where(users.c.email == email)
	ResultProxy = connection.execute(query)
	result = ResultProxy.first()
	if not result or not bcrypt.checkpw(password.encode('utf-8'), result['password'].encode('utf-8')):
		return { "error": "bad login" }, 401

	access_token = create_access_token(identity=result['user_id'])

	return {
		"access_token": access_token
	}, 200

@app.route("/signup", methods=['POST'])
def signup():
	if not request.is_json:
		return { "error": "invalid JSON" }, 400

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

	query = db.select([users]).where(users.c.email == email)
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
		"access_token": access_token
	}, 200

app.run()