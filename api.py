from flask import Flask, jsonify, request, session
from flask_login import logout_user, LoginManager
#from flask.ext.session import Session
from flask_session import Session
from datetime import datetime
import utils
from cerberus import Validator
from queries import *
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity)
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

app = Flask(__name__)
app.secret = 'asdsdfsdfs13sdf_df%&'
SESSION_TYPE = 'memcache'

sess = Session()

app.config["JWT_SECRET_KEY"] = 'secret'

jwt = JWTManager(app)
login_manager = LoginManager()

adminAuth = []
#response = utils.Response()

#logout route
@app.route("/logout")
def logout():
    session.pop('email',None)
    
    return {"response":"user logged off"}



#courses query route
@app.route('/courses', methods=['POST'])
def courses():
	if request.method == 'POST':
		course_name = request.get_json()['course_name']
		feedback = queryCourse(course_name)
		return {"feedback":feedback}

	else:
		return {"response":"not a valid request"}


#courses discount query route
@app.route('/courses/discount', methods=['POST'])
def discount():
	if request.method == 'POST':
		course_name = request.get_json()['course_name']
		discount = request.get_json()['discount']
		feedback = queryDiscount(course_name, discount)
		return {"feedback":feedback}


	else:
		return {"response":"not a valid request"}


#course application route
@app.route('/application', methods=['POST'])
def application():
	if request.method == 'POST':
		course_name = request.get_json()['course_name']
		feedback = queryApplication(course_name)
		return {"feedback":feedback}


	else:
		return {"response":"not a valid request"}


#users feedback route
@app.route('/registration/feedback', methods=['POST'])
def feedback():
	if request.method == 'POST':
		interest = request.get_json()['interest']
		channel = request.get_json()['channel']
		feedback = feedBack(interest, channel)
		return {"feedback":feedback}


	else:
		return {"response":"not a valid request"}


#users payment document upload route
@app.route('/upload', methods=['POST'])
def upload():
	if request.method == 'POST':
		userId = request.form['user_id']#userID
		file = request.files['file']#the file
		email = request.form['email']#the userEmail
		password = request.form['password']#user password
		feedback,data = dashboardQuery(email, password)#authenticating user

		if feedback == "True":
			access_token = create_access_token(identity = {
				"name" : data['name'],
				"email": data['email'],
				"phone" : data['phone']
				})
			refresh_token = create_refresh_token(identity={
				"name" : data['name'],
				"email": data['email'],
				"phone" : data['phone']
				})
			print(access_token)
			feedback = verifyImage(file, userId)#verifying image validity
			return {"feedback":feedback}



		else:
			return {"response":"User not found"}


	else:
		return {"response":"not a valid request"}



#route to send user to dashboard after credentials verification and authentication
@app.route('/dashboard', methods=['POST'])
def dashboard():
	if request.method == 'POST':
		email = request.get_json()['email']
		password = request.get_json()['password']
		

		feedback, data = dashboardQuery(email, password)

		if feedback == 'True':
			session['email'] = email
			#print(session)
			access_token = create_access_token(identity = {
				"name" : data['name'],
				"email" : data['email'],
				"phone" : data['phone']
				})
			print(access_token)

			return {"response":"True"}

		else:
			return {"response":"False"}



	else:
		return {"response":"not a valid request"}



#tadmin authentication
@app.route('/admin', methods = ['POST'])
def admin():
	if request.method == 'POST':
		email = request.get_json()['email']
		password = request.get_json()['password']

		answer = giveAdminAccess(email, password)#request admin access

		if answer == 'User is admin':
			return {"feedback":answer}

		else:
			return {"feedback":answer}


	return response



#this function is a blueprint for giving admin users the admin priviledges
def giveAdminAccess(email, password):

	feedback, data = dashboardQuery(email, password)

	if feedback == "True":
		access_token = create_access_token(identity = {
			"name" : data['name'],
			"email" : data['email']
			})
		refresh_token = create_refresh_token(identity={
			"email": data['email']
			})
		print(access_token)

		answer = confirmAdmin(data['userID'])
		return answer

	else:
		answer = 'Not aunthenticated'


#admin route for querying all users in the database
@app.route('/admin/users', methods=['POST'])
def allUsers():

	if request.method == 'POST':
		email = request.get_json()['email']
		password = request.get_json()['password']

		answer = giveAdminAccess(email, password)

		if answer == 'User is admin':
			feedback = queryUsers()
			return {"feedback":feedback}

		else:
			feedback = {"message":"not authorized"}


	else:
		return {"response":"not a valid request"}




#admin route for querying specific user from the db
@app.route('/admin/user', methods=['POST'])
def findUser():
	if request.method == 'POST':
		email = request.get_json()['email']
		password = request.get_json()['password']
		user_id = request.get_json()['user_id']

		answer = giveAdminAccess(email, password)

		if answer == 'User is admin':
			feedback = queryUser(user_id)
			return {"feedback":feedback}

		else:
			return {"feedback":"not aunthorized"}

	else:
		return {"response":"not a valid request"}



#admin route for confirming the users' uploaded payment document
@app.route('/users/payment/confirm', methods=['POST'])
def confirmPayment():
	if request.method == 'POST':
		email = request.get_json()['email']
		password = request.get_json()['password']
		user_id = request.get_json()['user_id']

		answer = giveAdminAccess(email, password)#request admin access

		if answer == 'User is admin':
			confirm =  confirmUserPay(user_id)

			return {"response": confirm}

		else:
			return {"response":"not aunthorized"}


	else:
		return {"response":"not a valid request"}


#admin route for seaching a user via user email
@app.route('/users/search', methods = ['POST'])
def searchUser():
	if request.method == 'POST':
		email = request.get_json()['email']#admin email
		password = request.get_json()['password']#admin password
		user_email = request.get_json()['user_email']#user email
		answer = giveAdminAccess(email, password)#request admin access
		if answer == 'User is admin':
			feedback = queryUserEmail(user_email)#query user details using the email
			return {"feedback":feedback}

		else:
			return {"response":"not authorized"}

	else:
		return {"response":"not a valid request"}



#admin route for viewing courses in the db
@app.route('/admin/courses', methods = ['POST'])
def adminCourses():
	if request.method == 'POST':
		email = request.get_json()['email']
		password = request.get_json()['password']
		answer = giveAdminAccess(email, password)
		if answer == 'User is admin':
			feedback = queryCourses()

			return {"response":feedback}
		else:
			return {"response":"not authorized"}

	else:
		return {"response":"not a valid request"}





#this route give access to admin to update the discount details of the course with courseID
@app.route('/admin/courses/discount', methods = ['POST'])
def coursesDiscount():
	to_date = lambda s: datetime.strptime(s, '%d-%m-%Y')#setting date format
	
	
	discount_valid = {'discount':{'type':'string','required':True}}#validation rules
	end_valid = {'start_date': {'type': 'datetime','coerce': to_date}}
	active_discount = {'discount_on':{'type':"string"}}
	if request.method == 'POST':
		discount = request.get_json()['discount']#the discount amount
		discount_on = request.get_json()['discount_on']#discount on
		discount_ends = request.get_json()['discount_ends']#discound end
		course_id = request.get_json()['course_id']#course ID to be updated
		email = request.get_json()['email']#admin email
		password = request.get_json()['password']#admin password
		answer = giveAdminAccess(email, password)#requesting admin access
		if answer == 'User is admin':
			try:
				dis = Validator(discount_valid)
				disc = {"discount":discount}
				diss = dis.validate(disc)#validate discount input

				if diss:
					dison = Validator(active_discount)
					discon = {"discount_on":discount_on}
					disoon = dison.validate(discon)#validate input ofactive discount

					if disoon:
						disend = Validator(end_valid)
						disc_end = {"start_date":discount_ends}
						diseend = disend.validate(disc_end)#validating iput of discount end

						if diseend:
							feedback = updateCourse(course_id, discount, discount_on, discount_ends)#updating the course
							return {"feedback":feedback}



					else:
						return {"message":"course edited successfully"}

				else:
					return {"message":"course edited successfully"}

			except Exception as error:
				print(error)
				return {"feedback":str(error)}
		else:
			return {"feedback":"not authorized"}

	else:
		return {"response":"not a valid request"}



#this route allows admin to query course object using the course ID
@app.route('/admin/courses', methods = ['POST'])
def adminCourse():
	if request.method == 'POST':
		course_id = request.get_json()['course_id']#course ID input
		email = request.get_json()['email']#admin email input
		password = request.get_json()['password']#admin password input
		answer = giveAdminAccess(email, password)#request for admin access

		if answer == 'User is admin':
			feedback = queryAdminCourse(course_id)#calls the function to query course
			return {"feedback":feedback}
		else:
			return {"feedback":"not authorized"}

	else:
		return {"response":"not a valid request"}



#the route that allows admin to update or create a new course with course obj
@app.route('/admin/course/', methods = ['POST'])#route init
def adminCreateCourse():
	if request.method == 'POST':
		dataType = request.get_json()['type']#action to be carried out (create/edit)
		course_id = request.get_json()['course_id']#courseID
		syllabus = request.get_json()['syllabus']#course syllabus
		title = request.get_json()['title']#course title
		weekday_price = request.get_json()['weekday_price']#weekdayprice
		weekday_duration = request.get_json()['weekday_duration']#weekday duration
		weekday_starts = request.get_json()['weekday_starts']#weekday start date
		weekend_price = request.get_json()['weekend_price']#weekend price
		weekend_duration = request.get_json()['weekend_duration']#weekend duration
		weekend_starts = request.get_json()['weekend_starts']#weekend start date

		#try:
		syll = {"syllabus":{"required":True}}
		syll = Validator(syll)#validator class
		syll = syll.validate({"syllabus":syllabus})#validating the syllabus input

		titl = {"title":{"required":True, "minlength":10}}
		titl = Validator(titl)
		titl = titl.validate({"title":title})#validating the title input

		wkday = {"weekday_price":{"required":True,"type":"integer"}}
		wkday = Validator(wkday)
		wkday = wkday.validate({"weekday_price":weekday_price})#validating the weekday price input

		wkdduration = {"weekday_duration":{"type":"integer","required":True}}
		wkdduration = Validator(wkdduration)
		wkdduration = wkdduration.validate({"weekday_duration":weekday_duration})#validating the weekday duration

		wkndduration = {"weekend_duration":{"type":"integer","required":True}}
		wkndduration = Validator(wkndduration)
		wkndduration = wkndduration.validate({"weekend_duration":weekend_duration})#validating the weekend duration

		to_date = lambda s: datetime.strptime(s, '%d-%m-%Y')
		wkdaystr = {'weekday_starts': {'type': 'datetime','coerce': to_date,"required":True}}
		wkdaystr = Validator(wkdaystr)
		wkdaystr = wkdaystr.validate({"weekday_starts":weekday_starts})#validating the weekday start date 

		wkndstr = {'weekend_starts': {'type': 'datetime','coerce': to_date,"required":True}}
		wkndstr = Validator(wkndstr)
		wkndstr = wkndstr.validate({"weekend_starts":weekend_starts})#validating the weekend start date

	
		wknday = {"weekend_price":{"required":True,"type":"integer"}}
		wknday = Validator(wknday)
		wknday = wknday.validate({"weekend_price":weekend_price})#validating the weekend price

		if (syll and titl and wkday and wkdduration and wkndduration and wkdaystr and wkndstr and wknday) == True:#checking if all validation is met
			if dataType == 'create':
				feedback = storeCourseObj(syllabus,title,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts)#creating the course
				return {"feedback":feedback}

			elif dataType == 'edit':
				feedback = updateCourseObj(course_id,syllabus,title,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts)#editing the course
				return {"feedback":feedback}

			else:
				pass

		else:
			return {"response":"Invalid request input"}


	else:
		return {"response":"not a valid request"}





if __name__ == '__main__':
	app.secret_key = 'jwnrwnubnerigjw'#the api secret key for keeping session
	app.config['SESSION_TYPE'] = 'filesystem'#the api session type
	sess.init_app(app)#initializing the session
	#this part should be changed to run on the server.
	app.run(debug=True, port = 4567)
