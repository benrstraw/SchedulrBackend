import schedulr_config
from flask import Flask, request, abort, session, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import sqlalchemy as db
from sqlalchemy.dialects.mysql import insert
import json
import bcrypt
from email_validator import validate_email, EmailNotValidError
import toposort as ts

app = Flask(__name__)
app.config.from_object(schedulr_config.Config)
jwt = JWTManager(app)
engine = db.create_engine(schedulr_config.Config.DATABASE_URI)
connection = engine.connect()
metadata = db.MetaData()
courses = db.Table('courses', metadata, autoload=True, autoload_with=engine)
course_reqs = db.Table('course_reqs', metadata, autoload=True, autoload_with=engine)
programs = db.Table('programs', metadata, autoload=True, autoload_with=engine)
prog_reqs = db.Table('prog_reqs', metadata, autoload=True, autoload_with=engine)
reqsets = db.Table('reqsets', metadata, autoload=True, autoload_with=engine)
rs_reqs = db.Table('rs_reqs', metadata, autoload=True, autoload_with=engine)
users = db.Table('users', metadata, autoload=True, autoload_with=engine)
user_reqs = db.Table('user_reqs', metadata, autoload=True, autoload_with=engine)
user_taken = db.Table('user_taken', metadata, autoload=True, autoload_with=engine)

semesters = ['FALL', 'SPRING', 'SUMMER']
statuses = ['COMPLETE', 'INPROGRESS', 'PLANNED']
passing = ['C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+']

def get_nested_prereqs(cid, dep_graph):
	# Very important: many classes share the same prereqs, so we go down the same call tree multiple times.
	# Solution: if the course is also in the graph, skip it. This skips not only the course call, but also the call for all it's prereqs.
	# This is fine because if the course has already been called once, we've already processed all it's prereqs as well.
	if cid in dep_graph:
		return

	# Retrieve from the DB the list of course IDs for the *prerequisites* for the input course ID.
	sel = db.select([courses.c.course_id]).select_from(courses.join(course_reqs, courses.c.course_id == course_reqs.c.prereq_id)).where(course_reqs.c.course_id == cid)
	res = connection.execute(sel)
	db_out = res.fetchall()

	# For the input course ID key in the dep_graph dictionary, add the set of prerequisite course IDs as the value.
	dep_graph[cid] = {row['course_id'] for row in db_out}

	# Since the new prerequisites we just discovered may each have their own prereqs, recursively run the call for all the courses we just added.
	for rec in dep_graph[cid]:
		get_nested_prereqs(rec, dep_graph)

def build_deps_graph(uid):
	# Get IDs for all of the reqsets the user has added.
	sel = db.select([reqsets.c.rs_id]).select_from(reqsets.join(user_reqs, reqsets.c.rs_id == user_reqs.c.rs_id)).where(user_reqs.c.user_id == get_jwt_identity())
	res = connection.execute(sel)
	db_out = res.fetchall()
	rsids = [row['rs_id'] for row in db_out]

	# Retrieve the course IDs for all of the reqset requirements for the reqsets acquired in the previous step.
	sel = db.select([courses.c.course_id]).select_from(courses.join(rs_reqs, courses.c.course_id == rs_reqs.c.course_id)).where(rs_reqs.c.rs_id.in_(rsids))
	res = connection.execute(sel)
	db_out = res.fetchall()
	needed_courses = list(dict.fromkeys([row['course_id'] for row in db_out]))

	# Retrieve all of the required courses from the DB given the list of required course IDs.
	sel = db.select([courses]).where(courses.c.course_id.in_(needed_courses))
	res = connection.execute(sel)
	db_out = res.fetchall()	
	needed_courses = [(dict(row.items())) for row in db_out]

	res.close() # Close the DB connection, we're done with it!

	# Create an empty dictionary to hold the dependency graph.
	dep_graph = dict()

	# For each of the courses in the reqset, call the recursive function to find it's prereqs all the way to the bottom.
	for nc in needed_courses:
		get_nested_prereqs(nc['course_id'], dep_graph)

	return dep_graph

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

@app.route("/list_reqsets", methods=['GET'])
def list_reqsets():
	sel = db.select([reqsets])
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

@app.route("/get_reqset", methods=['GET'])
def get_reqset():
	rsid = request.args.get('rs_id')
	if not rsid:
		return { "error": "no rs_id" }, 400

	sel = db.select([reqsets]).where(reqsets.c.rs_id == rsid)
	res = connection.execute(sel)
	db_out = res.first()

	if not db_out:
		return { "error": "invalid reqset" }, 404

	reqset = dict(db_out.items())

	sel = db.select([courses]).select_from(courses.join(rs_reqs, courses.c.course_id == rs_reqs.c.course_id)).where(rs_reqs.c.rs_id == reqset['rs_id'])
	res = connection.execute(sel)
	db_out = res.fetchall()
	reqset['courses'] = [(dict(row.items())) for row in db_out]

	res.close()

	return reqset, 200

@app.route("/my_taken", methods=['GET', 'POST'])
@jwt_required
def my_taken():
	sel = db.select([courses, user_taken.c.semester, user_taken.c.year, user_taken.c.grade, user_taken.c.status]).select_from(courses.join(user_taken, courses.c.course_id == user_taken.c.course_id)).where(user_taken.c.user_id == get_jwt_identity())
	res = connection.execute(sel)
	db_out = res.fetchall()
	res.close()

	return jsonify([(dict(row.items())) for row in db_out]), 200

@app.route("/my_reqsets", methods=['GET', 'POST'])
@jwt_required
def my_reqsets():
	sel = db.select([reqsets]).select_from(reqsets.join(user_reqs, reqsets.c.rs_id == user_reqs.c.rs_id)).where(user_reqs.c.user_id == get_jwt_identity())
	res = connection.execute(sel)
	db_out = res.fetchall()

	userreqsets = [(dict(row.items())) for row in db_out]

	# for u in userreqsets:
	# 	sel = db.select([courses]).select_from(courses.join(rs_reqs, courses.c.course_id == rs_reqs.c.course_id)).where(rs_reqs.c.rs_id == u['rs_id'])
	# 	res = connection.execute(sel)
	# 	db_out = res.fetchall()
	# 	u['courses'] = [(dict(row.items())) for row in db_out]

	res.close()

	return jsonify(userreqsets), 200

@app.route("/my_needed", methods=['GET', 'POST'])
@jwt_required
def my_needed():
	# Get IDs for all of the reqsets the user has added.
	sel = db.select([reqsets.c.rs_id]).select_from(reqsets.join(user_reqs, reqsets.c.rs_id == user_reqs.c.rs_id)).where(user_reqs.c.user_id == get_jwt_identity())
	res = connection.execute(sel)
	db_out = res.fetchall()
	rsids = [row['rs_id'] for row in db_out]

	# Retrieve the course IDs for all of the reqset requirements for the reqsets acquired in the previous step.
	sel = db.select([courses.c.course_id]).select_from(courses.join(rs_reqs, courses.c.course_id == rs_reqs.c.course_id)).where(rs_reqs.c.rs_id.in_(rsids))
	res = connection.execute(sel)
	db_out = res.fetchall()
	needed_courses = list(dict.fromkeys([row['course_id'] for row in db_out]))

	# Retrieve the course IDs, grades, and statuses for all the courses the user has taken.
	sel = db.select([courses.c.course_id, user_taken.c.grade, user_taken.c.status]).select_from(courses.join(user_taken, courses.c.course_id == user_taken.c.course_id)).where(user_taken.c.user_id == get_jwt_identity())
	res = connection.execute(sel)
	db_out = res.fetchall()

	# Compare the taken courses against the pass requirements, and remove passed course IDs from the list of required course IDs.
	userpassed = [(dict(row.items())) for row in db_out]
	for t in userpassed:
		if t['status'] == 'COMPLETE' and t['grade'] in passing:
			try:
				needed_courses.remove(t['course_id'])
			except ValueError as e:
				pass

	# Retrieve all of the required courses from the DB given the list of required course IDs.
	sel = db.select([courses]).where(courses.c.course_id.in_(needed_courses))
	res = connection.execute(sel)
	db_out = res.fetchall()	
	needed_courses = [(dict(row.items())) for row in db_out]

	res.close()

	return jsonify(needed_courses), 200

@app.route("/gen_schedule", methods=['GET', 'POST'])
@jwt_required
def gen_schedule():
	max_classes = 4

	if request.is_json:
		max_classes = request.json.get('max_classes')

	dep_graph = build_deps_graph(get_jwt_identity())

	# Run topological sort on the final dependency graph.
	toposorted = ts.toposort(dep_graph, max_classes)
	course_groups = [list(row) for row in toposorted]

	output = []
	for cg in course_groups:
		# Retrieve all of the required courses from the DB given the list of required course IDs.
		sel = db.select([courses]).where(courses.c.course_id.in_(cg))
		res = connection.execute(sel)
		db_out = res.fetchall()	
		output += [[(dict(row.items())) for row in db_out]]

	return jsonify(output), 200

@app.route("/add_taken", methods=['POST'])
@jwt_required
def add_taken():
	if not request.is_json:
		return { "error": "invalid JSON" }, 400

	cid = request.json.get('course_id')
	semester = request.json.get('semester').upper()
	year = request.json.get('year')
	grade = request.json.get('grade')
	status = request.json.get('status').upper()

	if not cid:
		return { "error": "no course_id" }, 400
	if not semester:
		return { "error": "no semester" }, 400
	if not year:
		return { "error": "no year" }, 400
	if not status:
		return { "error": "no status" }, 400

	if semester not in semesters:
		return { "error": "invalid semester (must be in ['FALL', 'SPRING', 'SUMMER'])" }, 400
	if status not in statuses:
		return { "error": "invalid semester (must be in ['COMPLETE', 'INPROGRESS', 'PLANNED'])" }, 400

	query = insert(user_taken).values(user_id=get_jwt_identity(), course_id=cid, semester=semester, year=year, grade=grade, status=status).on_duplicate_key_update(grade=grade, status=status)
	ResultProxy = connection.execute(query)

	return {}, 200

@app.route("/add_program", methods=['POST'])
@jwt_required
def add_program():
	if not request.is_json:
		return { "error": "invalid JSON" }, 400

	pid = request.json.get('prog_id')
	if not pid:
		return { "error": "no prog_id" }, 400

	sel = db.select([prog_reqs]).where(prog_reqs.c.prog_id == pid)
	res = connection.execute(sel)
	db_out = res.fetchall()

	rids = [(dict(row.items())) for row in db_out]
	for rs in rids:
		query = user_reqs.insert().values(user_id=get_jwt_identity(), rs_id=rs['rs_id']).prefix_with('IGNORE')
		ResultProxy = connection.execute(query)

	return {}, 200

@app.route("/add_reqset", methods=['POST'])
@jwt_required
def add_reqset():
	if not request.is_json:
		return { "error": "invalid JSON" }, 400

	rsid = request.json.get('rs_id')
	if not rsid:
		return { "error": "no rs_id" }, 400

	query = user_reqs.insert().values(user_id=get_jwt_identity(), rs_id=rsid).prefix_with('IGNORE')
	res = connection.execute(query)

	return {}, 200

@app.route("/drop_taken", methods=['POST'])
@jwt_required
def drop_taken():
	if not request.is_json:
		return { "error": "invalid JSON" }, 400

	cid = request.json.get('course_id')
	semester = request.json.get('semester').upper()
	year = request.json.get('year')

	if not cid:
		return { "error": "no course_id" }, 400
	if not semester:
		return { "error": "no semester" }, 400
	if not year:
		return { "error": "no year" }, 400

	if semester not in semesters:
		return { "error": "invalid semester (must be in ['FALL', 'SPRING', 'SUMMER'])" }, 400

	sel = user_taken.delete().where(db.and_(user_taken.c.user_id == get_jwt_identity(), user_taken.c.course_id == cid, user_taken.c.semester == semester, user_taken.c.year == year))
	res = connection.execute(sel)

	return {}, 200

@app.route("/drop_reqset", methods=['POST'])
@jwt_required
def drop_reqset():
	if not request.is_json:
		return { "error": "invalid JSON" }, 400

	rsid = request.json.get('rs_id')
	if not rsid:
		return { "error": "no rs_id" }, 400

	sel = user_reqs.delete().where(db.and_(user_reqs.c.user_id == get_jwt_identity(), user_reqs.c.rs_id == rsid))
	res = connection.execute(sel)

	return {}, 200

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

if __name__ == '__main__':
	app.run()