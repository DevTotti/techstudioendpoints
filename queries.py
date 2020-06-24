#############################

import mysql.connector as mysql
from datetime import datetime
import os, imghdr, random

import smtplib, ssl

##############################


#######################
#The emailsender and receiver credentials setup
########################

port = 465  
smtp_server = "smtp.gmail.com"
sender_email = ""  #insert the sender email
receiver_email = ""  #insert the receiver email here
password = #insert the sender email password here


######################

#Database connection

try:
	conn = mysql.connect(database = 'techStudio', user = 'root', host = 'localhost', password = 'postman')# edit the database connection credentials, host and database name
	cursor = conn.cursor(buffered=True, dictionary=True)
	print("connected Successfully!")

except Exception as error:
	print(error)

####################




#function for querying the course from the database, returns an object of the course or course not found
def queryCourse(name):
	course_name = str(name)
	print(course_name)

	query = """SELECT title FROM COURSE WHERE name = '{}'""".format(course_name)
	cursor.execute(query)
	count = cursor.fetchone()
	print(count)
	count = len(count)

	if count > 0:
		response = {"course":course_name}

	else:
		response = "course is not found"


	return response




#function that checks the input discount and queries the discont if active or not, returns active or expired
def queryDiscount(course, disc):
	course_name = course
	discount = disc

	if 'k' in discount:
		discount = discount.replace("k","000")


		query = """SELECT discount, discount_ends FROM COURSE WHERE COURSE.name = '{}'""".format(course_name)
		cursor.execute(query)

		for row in cursor.fetchall():
			db_discount = row['discount']
			discount_ends = row['discount_ends']

			if discount == db_discount and discount_ends != 'expired':
				response = "'countdown' is active"

			else:
				response = "'countdown' expired"


	else:
		response = "discount is false"


	return response




#the function that checks to see if a course name exists in the database
def queryApplication(course):
	course_name = course

	query = """SELECT * FROM COURSE WHERE name = '{}'""".format(course_name)
	count = cursor.execute(query)
	count = len(cursor.fetchone())

	if count > 0:
		response = course_name

	else:
		response = "'course' not found"


	return response


#this function saves the feedback of users on the website into the database, returns feedback saved or not saved
def feedBack(interests, channels):
	interest = interests
	channel = channels

	query = """INSERT into REGISTRATION_FEEDBACKS (interest, channel) values ('{}','{}')""".format(interest, channel)
	try:
		cursor.execute(query)
		conn.commit()
		response = "'feedback' saved"
		return response

	except Exception as error:
		response = "'feedback' not saved"
		return response



#this fnction qeries all the users in the database, returns a list of all the users
def queryUsers():
	users = []
	query = """SELECT * FROM USER """
	cursor.execute(query)

	for row in cursor.fetchall():
		name = row['name']
		users.append(name)


	return users



#thisfunction returns the object containing name, email and phone of a user queried from the database
def queryUser(user_id):
	userID = user_id

	query = """SELECT * FROM USER WHERE id = {}""".format(userID)
	try:
		cursor.execute(query)

		for row in cursor.fetchall():
			name = row['name']
			email = row['email']
			phone = row['phone']


			user = {"name":name, "email":email, "phone":phone}


			return user

	except:
		return {"message":"user not in db"}




#this function finds a user with a specific email from the database, retrns if user is found or not
def queryUserEmail(user_email):
	userEmail = user_email

	query = """SELECT name FROM USER WHERE USER.email = '{}'""".format(userEmail)
	cursor.execute(query)
	count = cursor.fetchone()
	try:
		user = count['name']

		if user:
			response = {"user":user}

		else:
			response = "User not found"

		return response

	except:
		return {"response":"no user found"}



#this function returns all the courses available in the database
def queryCourses():
	courses = []
	query = """SELECT * FROM COURSE"""
	cursor.execute(query)

	for row in cursor.fetchall():
		course = row['title']
		courses.append(course)


	return courses




#this function verifies user credentials, authenticate it and returns true or false
def dashboardQuery(email, password):
	mail = email
	passwd = password

	query = """SELECT * FROM USER WHERE email = '{}'""".format(mail)
	try:
		cursor.execute(query)



		for row in cursor.fetchall():
			password = row['password']
			userID = row['id']
			name = row['name']
			email = row['email']
			phone = row['phone']

			if str(password) == passwd:
				print("Password match")
				data = {"name":name, "email": email, "phone": phone, "userID": userID}
				response = ("True", data)
				return response

			else:
				print("Password mismatch")
				response = ("False", userID)
				return response

	except Exception as error:
		response = ("False", mail)
		return response




#this function verifies the payment receipt in form of image uploaded by the user and sends a mail to admin to confirm payment
def verifyImage(file, user_id):
	imgfile = file
	userID = user_id
	data = imghdr.what(imgfile)
	timenow = datetime.now()
	timestmp = timenow.time()
	timeFile = str(timestmp.hour)+":"+str(timestmp.minute)+":"+str(timestmp.second)
	randFile = random.randint(1,10)

	timeFile = timeFile + str(randFile)

	if data == 'png' or data == 'jpeg':
		print("Valid File")
		imgfile.filename = str(timeFile)
		imagePath = "C:/Users/HP/Documents/techAcademy/docs"
		try:
			query = """INSERT INTO PAYMENT_DETAILS (user_id,image_path,amount_paid, amount_remaining) values('{}','{}','{}','{}')""".format(userID, imagePath, 50000, 10000)
			cursor.execute(query)
			conn.commit()
			print("successfully")

			try:
				message = """\
				Subject: Payment Document Uploaded

				Te payment document for user {} has been uploaded succssfuy
				""".format(userID)

				context = ssl.create_default_context()
				with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
					server.login(sender_email, password)
					server.sendmail(sender_email, receiver_email, message)

				response = {"messsage": "document uploaded successfully."}

				return response

			except Exception as error:
				response = {"feedback":str(error)}
				print(response)
				return response

			


		except Exception as error:
			response = {"message":"Failed"}
			return response


	else:
		print("Invalid File")
		response = False



#this function admin credentials and authorizes
def confirmAdmin(user_id):
	userID = user_id
	query = """SELECT USER_ROLE.role_id from USER_ROLE INNER JOIN USER ON USER.id=USER_ROLE.user_id WHERE USER.id = '{}'""".format(userID)
	cursor.execute(query)
	count =  cursor.fetchone()
	role_id = count['role_id']

	if role_id == 1:
		response = 'User is admin'
	else:
		response = 'User is not admin'


	return response



#this function gives admin the access to confirm if user has paid
def confirmUserPay(user_id):
	userID = user_id
	query = """SELECT * FROM PAYMENT_DETAILS WHERE user_id = {}""".format(userID)
	cursor.execute(query)
	count = cursor.fetchone()

	if len(count) > 0:
		response = "Payment confirmed"

	else:
		response = "No payment"

	return response


#this function gives admin access to update courses in the COURSE database
def updateCourse(course_id, discount, discount_on, discount_ends):
	courseID = course_id
	disc = discount
	discON = discount_on
	discEND = discount_ends

	query = """UPDATE COURSE SET discount = '{}', discount_ends = '{}', discount_on = '{}' WHERE COURSE.id = {}""".format(disc, discEND, discON, courseID)
	try:
		cursor.execute(query)
		response = {"message":"course edited successfully"}
		return response

	except Exception as error:
		response = {"message":"course not updated"}
		return response







#this function allows admin to query course using the course ID and returns the course object if found
def queryAdminCourse(course_id):
	courseID = course_id

	try:
		query = """SELECT * FROM COURSE WHERE COURSE.id = {}""".format(courseID)
		cursor.execute(query)
		for row in cursor.fetchall():
			ids = row['id']
			title = row['title']
			name = row['name']


			courseObj = {"courseID":ids, "courseTitle":title, "courseName":name}


		return courseObj

	except Exception as error:
		return {"messgae":"course not found"}






#this fnction allows admin to save course into the database
def storeCourseObj(syllabus,title,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts):
	query = """INSERT INTO COURSE (syllabus,title,name,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts)
				values ('{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(syllabus,title,title,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts)
	try:
		cursor.execute(query)
		return "course created"

	except Exception as error:
		print(error)
		return "course not created"



#this function allows admin to update courses in the database
def updateCourseObj(course_id,syllabus,title,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts):
	query = """UPDATE COURSE SET syllabus = '{}',title = '{}', name = '{}' ,weekday_price = '{}',weekday_duration = '{}',weekday_starts = '{}',weekend_price = '{}',weekend_duration = '{}',weekend_starts = '{}' WHERE course_id = '{}'""".format(syllabus,title,title,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts,course_id)
	try:
		cursor.execute(query)
		return "course edited successfully"

	except Exception as error:
		return "course not edited"


