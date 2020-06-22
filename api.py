from flask import Flask, jsonify, request, render_template, session
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

#
@app.route("/logout")
def logout():
    session.pop('email',None)
    
    return "user logged off"



#tested, perfect
@app.route('/courses', methods=['POST'])
def courses():
	if request.method == 'POST':
		course_name = request.get_json()['course_name']
		feedback = queryCourse(course_name)
		return feedback

	else:
		return ('not a valid request')


#tested, perfect
@app.route('/courses/discount', methods=['POST'])
def discount():
	if request.method == 'POST':
		course_name = request.get_json()['course_name']
		discount = request.get_json()['discount']
		feedback = queryDiscount(course_name, discount)
		return feedback


	else:
		return ('not a valid request')


#tested, perfect
@app.route('/application', methods=['POST'])
def application():
	if request.method == 'POST':
		course_name = request.get_json()['course_name']
		feedback = queryApplication(course_name)
		return feedback


	else:
		return ('not a valid request')


#tested, perfect
@app.route('/registration/feedback', methods=['POST'])
def feedback():
	if request.method == 'POST':
		interest = request.get_json()['interest']
		channel = request.get_json()['channel']
		feedback = feedBack(interest, channel)
		return feedback


	else:
		return ('not a valid request')



@app.route('/upload', methods=['POST'])
def upload():
	if request.method == 'POST':
		userId = request.get_json()['user_id']
		interest = request.files['image']
		email = request.get_json()['email']
		password = request.get_json()['password']
		feedback = dashboardQuery(email, password)

		if feedback == "True":
			access_token = create_access_token(identity = {
				"name" : feedback['name'],
				"email": feedback['email'],
				"phone" : feedback['phone']
				})
			refresh_token = create_refresh_token(identity={
				"name" : feedback['name'],
				"email": feedback['email'],
				"phone" : feedback['phone']
				})
			print(access_token)
			feedback = verifyImage(file, userID)
			return feedback



		else:
			return "User not found"


	else:
		return ('not a valid request')



#tested, perfect
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

			return "True"

		else:
			return "False"



	else:
		return ('not a valid request')



#tested, perfect
@app.route('/admin', methods = ['POST'])
def admin():
	if request.method == 'POST':
		email = request.get_json()['email']
		password = request.get_json()['password']

		answer = giveAdminAccess(email, password)

		if answer == 'User is admin':
			return {"feedback":answer}

		else:
			return {"feedback":answer}


	return response



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


#tested, perfect
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
		return ('not a valid request')




#tested, perfect
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
		return ('not a valid request')
	

#tested, perfect
@app.route('/users/payment/confirm', methods=['POST'])
def confirmPayment():
	if request.method == 'POST':
		email = request.get_json()['email']
		password = request.get_json()['password']
		user_id = request.get_json()['user_id']

		answer = giveAdminAccess(email, password)

		if answer == 'User is admin':
			confirm =  confirmUserPay(user_id)

			return {"response": confirm}

		else:
			return {"response":"not aunthorized"}


	else:
		return ('not a valid request')


#tested, perfect
@app.route('/users/search', methods = ['POST'])
def searchUser():
	if request.method == 'POST':
		email = request.get_json()['email']
		password = request.get_json()['password']
		user_email = request.get_json()['user_email']
		answer = giveAdminAccess(email, password)
		if answer == 'User is admin':
			feedback = queryUserEmail(user_email)
			return feedback

		else:
			return {"response":"not authorized"}

	else:
		return ('not a valid request')



#tested, perfect
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
		return ('not a valid request')





#tested, perfect
@app.route('/admin/courses/discount', methods = ['POST'])
def coursesDiscount():
	to_date = lambda s: datetime.strptime(s, '%d-%m-%Y')
	
	#v.validate({'start_date': '2017-10-01'})
	discount_valid = {'discount':{'type':'string','required':True}}
	end_valid = {'start_date': {'type': 'datetime','coerce': to_date}}
	active_discount = {'discount_on':{'type':"string"}}
	if request.method == 'POST':
		discount = request.get_json()['discount']
		discount_on = request.get_json()['discount_on']
		discount_ends = request.get_json()['discount_ends']
		course_id = request.get_json()['course_id']
		email = request.get_json()['email']
		password = request.get_json()['password']
		answer = giveAdminAccess(email, password)
		if answer == 'User is admin':
			try:
				dis = Validator(discount_valid)
				disc = {"discount":discount}
				diss = dis.validate(disc)

				if diss:
					dison = Validator(active_discount)
					discon = {"discount_on":discount_on}
					disoon = dison.validate(discon)

					if disoon:
						disend = Validator(end_valid)
						disc_end = {"start_date":discount_ends}
						diseend = disend.validate(disc_end)

						if diseend:
							feedback = updateCourse(course_id, discount, discount_on, discount_ends)
							return feedback



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
		return ('not a valid request')


#tested, perfect
@app.route('/admin/courses', methods = ['POST'])
def adminCourse():
	if request.method == 'POST':
		course_id = request.get_json()['course_id']
		email = request.get_json()['email']
		password = request.get_json()['password']
		answer = giveAdminAccess(email, password)

		if answer == 'User is admin':
			feedback = queryAdminCourse(course_id)
			return {"feedback":feedback}
		else:
			return {"feedback":"not authorized"}

	else:
		return ('not a valid request')




@app.route('/admin/course/', methods = ['POST'])
def adminCreateCourse():
	if request.method == 'POST':
		dataType = request.get_json()['type']
		course_id = request.get_json()['course_id']
		syllabus = request.get_json()['syllabus']
		title = request.get_json()['title']
		weekday_price = request.get_json()['weekday_price']
		weekday_duration = request.get_json()['weekday_duration']
		weekday_starts = request.get_json()['weekday_starts']
		weekend_price = request.get_json()['weekend_price']
		weekend_duration = request.get_json()['weekend_duration']
		weekend_starts = request.get_json()['weekend_starts']

		#try:
		syll = {"syllabus":{"required":True}}
		syll = Validator(syll)
		syll = syll.validate({"syllabus":syllabus})

		titl = {"title":{"required":True, "minlength":10}}
		titl = Validator(titl)
		titl = titl.validate({"title":title})

		wkday = {"weekday_price":{"required":True,"type":"integer"}}
		wkday = Validator(wkday)
		wkday = wkday.validate({"weekday_price":weekday_price})

		wkdduration = {"weekday_duration":{"type":"integer","required":True}}
		wkdduration = Validator(wkdduration)
		wkdduration = wkdduration.validate({"weekday_duration":weekday_duration})

		wkndduration = {"weekend_duration":{"type":"integer","required":True}}
		wkndduration = Validator(wkndduration)
		wkndduration = wkndduration.validate({"weekend_duration":weekend_duration})

		to_date = lambda s: datetime.strptime(s, '%d-%m-%Y')
		wkdaystr = {'weekday_starts': {'type': 'datetime','coerce': to_date,"required":True}}
		wkdaystr = Validator(wkdaystr)
		wkdaystr = wkdaystr.validate({"weekday_starts":weekday_starts})

		wkndstr = {'weekend_starts': {'type': 'datetime','coerce': to_date,"required":True}}
		wkndstr = Validator(wkndstr)
		wkndstr = wkndstr.validate({"weekend_starts":weekend_starts})

	
		wknday = {"weekend_price":{"required":True,"type":"integer"}}
		wknday = Validator(wknday)
		wknday = wknday.validate({"weekend_price":weekend_price})

		if (syll and titl and wkday and wkdduration and wkndduration and wkdaystr and wkndstr and wknday) == True:
			if dataType == 'create':
				feedback = storeCourseObj(syllabus,title,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts)
				return {"feedback":feedback}

			elif dataType == 'edit':
				feedback = updateCourseObj(course_id,syllabus,title,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts)
				return {"feedback":feedback}

			else:
				pass

		else:
			return "Invalid request input"

		#except Exception as error:
		#	print(error)
		#	return {"feedback":str(error)}

	else:
		return ('not a valid request')





if __name__ == '__main__':
	app.secret_key = 'jwnrwnubnerigjw'
	app.config['SESSION_TYPE'] = 'filesystem'
	sess.init_app(app)
	app.run(debug=True, port = 4567)
