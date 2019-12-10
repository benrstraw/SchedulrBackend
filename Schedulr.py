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
user_progs = db.Table('user_progs', metadata, autoload=True, autoload_with=engine)
user_taken = db.Table('user_taken', metadata, autoload=True, autoload_with=engine)

# Valid semesters and statuses for course attempts.
semesters = ['FALL', 'SPRING', 'SUMMER']
statuses = ['COMPLETE', 'INPROGRESS', 'PLANNED']

# The course grades which are considered passing.
passing = ['C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+']

#####
# A recursive function which obtains the prerequisites for a course, then calls itself on those prerequisites as well.
# This builds a directed graph of every course that the user will have to take to complete their requirements sets.
# The paramaters are a course_id, the dependency graph, and a list of the courses the user has passed. Returns nothing.
def get_nested_prereqs(cid, dep_graph, userpass):
	# Very important: many classes share the same prereqs, so we go down the same call tree multiple times.
	# Solution: if the course is also in the graph, skip it. This skips not only the course call, but also the call for all it's prereqs.
	# This is fine because if the course has already been called once, we've already processed all it's prereqs as well.
	# ALSO, we do not want to add classes that have already been passed, this will create incorrect semester plans.
	if cid in dep_graph or cid in userpass:
		return

	# Retrieve from the DB the list of course IDs for the *prerequisites* for the input course ID.
	sel = db.select([courses.c.course_id]).select_from(courses.join(course_reqs, courses.c.course_id == course_reqs.c.prereq_id)).where(course_reqs.c.course_id == cid)
	res = connection.execute(sel)
	db_out = res.fetchall()

	# For the input course ID key in the dep_graph dictionary, add the set of prerequisite course IDs as the value.
	# If the class has already been passsed, it's no longer a required prerequisite and is dropped.
	dep_graph[cid] = {row['course_id'] for row in db_out if row['course_id'] not in userpass}

	# Since the new prerequisites we just discovered may have their own prereqs, recursively call on the new courses.
	for rec in dep_graph[cid]:
		get_nested_prereqs(rec, dep_graph, userpass)

#####
# The caller function for the recursive get_nested_prereqs(), this function returns a directed dependency graph of all
# the courses the user must take to complete their requirements sets. The input paramaters are the user_id of the user,
# and optionally a boolean stating whether we should ignore the user's passed courses and build the entire program.
def build_deps_graph(uid, ignore_passed = False):
	# Get IDs for all of the reqsets the user has added.
	sel = db.select([reqsets.c.rs_id]).select_from(reqsets.join(prog_reqs.join(user_progs, prog_reqs.c.prog_id == user_progs.c.prog_id), reqsets.c.rs_id == prog_reqs.c.rs_id)).where(user_progs.c.user_id == get_jwt_identity())
	res = connection.execute(sel)
	db_out = res.fetchall()
	rsids = [row['rs_id'] for row in db_out]

	# Retrieve the course IDs for all of the reqset requirements for the reqsets acquired in the previous step.
	sel = db.select([courses.c.course_id]).select_from(courses.join(rs_reqs, courses.c.course_id == rs_reqs.c.course_id)).where(rs_reqs.c.rs_id.in_(rsids))
	res = connection.execute(sel)
	db_out = res.fetchall()
	needed_courses = list(dict.fromkeys([row['course_id'] for row in db_out]))

	# Retrieve the course IDs, grades, and statuses for all the courses the user has taken.
	sel = db.select([courses.c.course_id, user_taken.c.grade, user_taken.c.status]).select_from(courses.join(user_taken, courses.c.course_id == user_taken.c.course_id)).where(user_taken.c.user_id == uid)
	res = connection.execute(sel)
	db_out = res.fetchall()

	res.close() # Close the DB connection, we're done with it!

	# Compare the taken courses against the pass requirements, and remove passed course IDs from the list of required course IDs.
	usertake = [(dict(row.items())) for row in db_out]
	userpass = []
	for t in usertake:
		if t['status'] == 'COMPLETE' and t['grade'] in passing:
			userpass += [t['course_id']]

	# Create an empty dictionary to hold the dependency graph.
	dep_graph = dict()

	# For each of the courses in the reqset, call the recursive function to find it's prereqs all the way to the bottom.
	for nc in needed_courses:
		if ignore_passed:
			get_nested_prereqs(nc, dep_graph, [])
		else:
			get_nested_prereqs(nc, dep_graph, userpass)

	return dep_graph

### Auth checker
@app.route("/auth", methods=['GET'])
@jwt_required
def auth():
	return {
		"user_id": get_jwt_identity()
	}, 200

#####
# Simple SELECT * FROM courses route.
@app.route("/list_courses", methods=['GET'])
def list_courses():
	# SELECT * FROM courses;
	sel = db.select([courses])
	res = connection.execute(sel)
	db_out = res.fetchall()
	res.close()
	return jsonify([(dict(row.items())) for row in db_out]), 200

#####
# Simple SELECT * FROM programs route.
@app.route("/list_programs", methods=['GET'])
def list_programs():
	# SELECT * FROM programs;
	sel = db.select([programs])
	res = connection.execute(sel)
	db_out = res.fetchall()
	res.close()
	return jsonify([(dict(row.items())) for row in db_out]), 200

#####
# Simple SELECT * FROM reqsets route.
@app.route("/list_reqsets", methods=['GET'])
def list_reqsets():
	# SELECT * FROM reqsets;
	sel = db.select([reqsets])
	res = connection.execute(sel)
	db_out = res.fetchall()
	res.close()
	return jsonify([(dict(row.items())) for row in db_out]), 200

#####
# Route which retrieves information about a course, and a list of all of it's prerequisites.
@app.route("/get_course", methods=['GET'])
def get_course():
	cid = request.args.get('course_id')
	if not cid:
		return { "error": "no course_id" }, 400

	# SELECT * FROM courses WHERE course_id = {cid};
	sel = db.select([courses]).where(courses.c.course_id == cid)
	res = connection.execute(sel)
	db_out = res.first()

	if not db_out:
		return { "error": "invalid course" }, 404

	# We only grabbed the first result from the DB call, turn it into just a dictionary.
	course_info = dict(db_out.items())

	# SELECT courses.* FROM courses c JOIN course_reqs cr ON c.course_id = cr.prereq_id WHERE c.course_id = {cid};
	sel = db.select([courses]).select_from(courses.join(course_reqs, courses.c.course_id == course_reqs.c.prereq_id)).where(course_reqs.c.course_id == cid)
	res = connection.execute(sel)
	db_out = res.fetchall()

	# Add to the course dictionary an array of other course dictionaries.
	course_info['prereqs'] = [(dict(row.items())) for row in db_out]

	res.close()

	return course_info, 200

#####
# Route which retrieves information about a reqset, and a list of all of it's contained courses.
@app.route("/get_reqset", methods=['GET'])
def get_reqset():
	rsid = request.args.get('rs_id')
	if not rsid:
		return { "error": "no rs_id" }, 400

	# SELECT * FROM reqsets WHERE rs_id = {rsid};
	sel = db.select([reqsets]).where(reqsets.c.rs_id == rsid)
	res = connection.execute(sel)
	db_out = res.first()

	if not db_out:
		return { "error": "invalid reqset" }, 404

	# Make a dictionary from the single response of the first DB call.
	reqset = dict(db_out.items())

	# SELECT courses.* FROM courses c JOIN rs_reqs rs ON c.course_id = rs.course_id WHERE rs.rs_id = {rsid};
	sel = db.select([courses]).select_from(courses.join(rs_reqs, courses.c.course_id == rs_reqs.c.course_id)).where(rs_reqs.c.rs_id == reqset['rs_id'])
	res = connection.execute(sel)
	db_out = res.fetchall()

	# Add the returned courses as an array of dictionaries.
	reqset['courses'] = [(dict(row.items())) for row in db_out]

	res.close()

	return reqset, 200

#####
# Route which retrieves all of the take-attempts of a user, including course info, year and semester attempted,
# status, and grade.
@app.route("/my_taken", methods=['GET', 'POST'])
@jwt_required
def my_taken():
	# SELECT courses.*, user_taken.semester, user_taken.year, user_taken.grade, user_taken.status FROM courses c JOIN user_taken ut ON c.course_id = ut.course_id WHERE ut.user_id = {uid};
	sel = db.select([courses, user_taken.c.semester, user_taken.c.year, user_taken.c.grade, user_taken.c.status]).select_from(courses.join(user_taken, courses.c.course_id == user_taken.c.course_id)).where(user_taken.c.user_id == get_jwt_identity())
	res = connection.execute(sel)
	db_out = res.fetchall()
	res.close()

	return jsonify([(dict(row.items())) for row in db_out]), 200

#####
# Route which returns information about all of the requirements sets a user has added to their account.
@app.route("/my_reqsets", methods=['GET', 'POST'])
@jwt_required
def my_reqsets():
	# SELECT r.* FROM schedulr.reqsets r JOIN schedulr.prog_reqs pr ON r.rs_id = pr.rs_id JOIN schedulr.user_progs up ON up.prog_id = pr.prog_id WHERE up.user_id = {uid}
	sel = db.select([reqsets]).select_from(reqsets.join(prog_reqs.join(user_progs, prog_reqs.c.prog_id == user_progs.c.prog_id), reqsets.c.rs_id == prog_reqs.c.rs_id)).where(user_progs.c.user_id == get_jwt_identity())
	res = connection.execute(sel)
	db_out = res.fetchall()

	userreqsets = [(dict(row.items())) for row in db_out]

	###
	# This used to return all of the courses contained within each reqset, but this was deemed too unweildy.
	# It's possible this functionality may be returned in a future API version at request of the front-end team.

	# for u in userreqsets:
	# 	sel = db.select([courses]).select_from(courses.join(rs_reqs, courses.c.course_id == rs_reqs.c.course_id)).where(rs_reqs.c.rs_id == u['rs_id'])
	# 	res = connection.execute(sel)
	# 	db_out = res.fetchall()
	# 	u['courses'] = [(dict(row.items())) for row in db_out]

	res.close()

	return jsonify(userreqsets), 200

#####
# Route which returns information about all of the requirements sets a user has added to their account.
@app.route("/my_programs", methods=['GET', 'POST'])
@jwt_required
def my_programs():

	sel = db.select([programs]).select_from(programs.join(user_progs, programs.c.prog_id == user_progs.c.prog_id)).where(user_progs.c.user_id == get_jwt_identity())
	res = connection.execute(sel)
	db_out = res.fetchall()

	userprogs = [(dict(row.items())) for row in db_out]

	res.close()

	return jsonify(userprogs), 200

#####
# Retrieve a list of all the courses the user must still pass to complete their requirements sets.
@app.route("/my_needed", methods=['GET', 'POST'])
@jwt_required
def my_needed():
	# Get IDs for all of the reqsets the user has added.
	sel = db.select([reqsets]).select_from(reqsets.join(prog_reqs.join(user_progs, prog_reqs.c.prog_id == user_progs.c.prog_id), reqsets.c.rs_id == prog_reqs.c.rs_id)).where(user_progs.c.user_id == get_jwt_identity())
	res = connection.execute(sel)
	db_out = res.fetchall()
	rss = [dict(row.items()) for row in db_out]

	# Retrieve the course IDs for all of the reqset requirements for the reqsets acquired in the previous step.
	sel = db.select([courses.c.course_id]).select_from(courses.join(rs_reqs, courses.c.course_id == rs_reqs.c.course_id)).where(rs_reqs.c.rs_id.in_([rs['rs_id'] for rs in rss]))
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

#####
# Generate a a list of lists of dictionaries, representing courses in a semester. The outer list acts as an ordered
# container for the inner lists, each of which represents a semester. Any of the courses within a semester may be
# attempted with each other, however the courses in a semester must all be completed before it is guarenteed the user
# has access to courses in a future semester. It may be the case that the user can take the courses out of order,
# since all of the requirements get bundled together, but we can only guarenteed prereqs have been satisfied if the
# entire semester is completed before moving on.
@app.route("/gen_schedule", methods=['GET', 'POST'])
@jwt_required
def gen_schedule():
	# Default max_classes to 4.
	max_classes = 4

	# If the user provided a JSON request and it contains a max_classes key, overwrite out default value.
	if request.is_json and 'max_classes' in request.json:
		max_classes = request.json.get('max_classes')

	# Build a dependency graph of all the courses the user must still take.
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

		# Add to the output all of the returned courses for this semester inside their own list (a semester).
		output += [[(dict(row.items())) for row in db_out]]

	return jsonify(output), 200

#####
# Add a course take-attempt to the user account. The take-attempts are internally identified by a
# (user_id, course_id, semester, year) primary key, which allows for duplicate attempts of a course across multiple
# semesters.
### If this route is called with an already existing primary key, the grade and status for that record will be updated!
### This allows the /add_taken route to be used to both add and modify!
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

	# Validate the enum inputs against the lists of valid inputs.
	if semester not in semesters:
		return { "error": "invalid semester (must be in ['FALL', 'SPRING', 'SUMMER'])" }, 400
	if status not in statuses:
		return { "error": "invalid semester (must be in ['COMPLETE', 'INPROGRESS', 'PLANNED'])" }, 400

	# Insert the user supplied values into the table, overwriting the non-PK values (grade and status) on duplicate.
	query = insert(user_taken).values(user_id=get_jwt_identity(), course_id=cid, semester=semester, year=year, grade=grade, status=status).on_duplicate_key_update(grade=grade, status=status)
	ResultProxy = connection.execute(query)

	return {
		"success": True
	}, 200

#####
# Add a program to the user account.
@app.route("/add_program", methods=['POST'])
@jwt_required
def add_program():
	if not request.is_json:
		return { "error": "invalid JSON" }, 400

	pid = request.json.get('prog_id')
	if not pid:
		return { "error": "no prog_id" }, 400

	query = user_progs.insert().values(user_id=get_jwt_identity(), prog_id=pid).prefix_with('IGNORE')
	res = connection.execute(query)

	return {
		"success": True
	}, 200

#####
# Remove a course take-attempt from the user account. Fails and incompletes should remain a part of the record.
# This route should only be used if a take-attempt is erroneously added.
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

	# Validate the enum inputs against the list of valid inputs.
	if semester not in semesters:
		return { "error": "invalid semester (must be in ['FALL', 'SPRING', 'SUMMER'])" }, 400

	sel = user_taken.delete().where(db.and_(user_taken.c.user_id == get_jwt_identity(), user_taken.c.course_id == cid, user_taken.c.semester == semester, user_taken.c.year == year))
	res = connection.execute(sel)

	return {
		"success": True
	}, 200

#####
# Removes a requirements set from the user account.
@app.route("/drop_program", methods=['POST'])
@jwt_required
def drop_reqset():
	if not request.is_json:
		return { "error": "invalid JSON" }, 400

	progid = request.json.get('prog_id')
	if not progid:
		return { "error": "no prog_id" }, 400

	sel = user_progs.delete().where(db.and_(user_progs.c.user_id == get_jwt_identity(), user_progs.c.prog_id == progid))
	res = connection.execute(sel)

	return {
		"success": True
	}, 200

#####
# Log into an existing user account.
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

	# 401 if there is no result from the users table for that email, or the bcrypyy check fails (incorrect password).
	if not result or not bcrypt.checkpw(password.encode('utf-8'), result['password'].encode('utf-8')):
		return { "error": "bad login" }, 401

	# Generate a new access_token for the user and return it. It is the API user's responsibility to store this.
	access_token = create_access_token(identity=result['user_id'])

	return {
		"access_token": access_token
	}, 200

#####
# Create a new user account.
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

	# Validate the email without checking if the domain is actually deliverable. On fail, 400.
	try:
		v = validate_email(email, check_deliverability=False)
		email = v['email']
	except EmailNotValidError as e:
		return { "error": "invalid email" }, 400

	# Select from the database with the email to check for duplicate accounts.
	query = db.select([users]).where(users.c.email == email)
	ResultProxy = connection.execute(query)
	result = ResultProxy.first()
	if result:
		return { "error": "email exists" }, 409

	# bcrypt hash the new account's password.
	hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

	# Insert the new account into the users table.
	query = users.insert().values(email=email, password=hashed, name=name)
	ResultProxy = connection.execute(query)

	# Capture the returned primary key (user_id) so we can generate an access token for it.
	user_id = ResultProxy.inserted_primary_key[0]

	# Return an access token for the new account so they don't have to log in right away.
	access_token = create_access_token(identity=user_id)

	return {
		"access_token": access_token
	}, 200

### Only run the internal Flask server if this file is being run as the main script.
if __name__ == '__main__':
	app.run()