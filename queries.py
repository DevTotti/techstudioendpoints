import mysql.connector as mysql
from datetime import datetime
import os, imghdr, random
import mysql.connector.cursor

import smtplib, ssl

port = 465  
smtp_server = "smtp.gmail.com"
sender_email = "iotweaks@gmail.com"  
receiver_email = "admin@gmail.com"  
#password = input("Type your email password and press enter: ")




try:
	conn = mysql.connect(database = 'techStudio', user = 'root', host = 'localhost', password = 'postman')
	cursor = conn.cursor(buffered=True, dictionary=True)
	print("connected Successfully!")

except Exception as error:
	print(error)



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



def queryDiscount(course, disc):
	course_name = course
	discount = disc

	if 'k' in discount:
		discount = discount.replace("k","000")


		query = """SELECT discount, discount_ends FROM COURSE WHERE COURSE.name = {}""".format(course_name)
		cursor.execute(query)

		for row in cursor.fetchall:
			db_discount = row[0]
			discount_ends = row[1]

			if discount == db_discount and discount_ends != 'expired':
				response = "'countdown' is active"

			else:
				response = "'countdown' expired"


	else:
		response = "discount is false"


	return response



def queryApplication(course):
	course_name = course

	query = """SELECT * FROM COURSE WHERE name = {}""".format(course_name)
	count = cursor.execute(query)

	if count > 0:
		response = course_name

	else:
		response = "'course' not found"


	return response



def feedBack(interests, channels):
	interest = interests
	channel = channels

	query = """INSERT into REGISTRATION_FEEDBACKS (interest, channel) values ({},{})""".format(interest, channel)
	try:
		cursor.execute(query)
		conn.commit()
		response = "'feedback' saved"
		return response

	except Exception as error:
		response = "'feedback' not saved"
		return response



def queryUsers():
	users = []
	query = """SELECT * FROM USER """
	cursor.execute(query)

	for row in cursor.fetchall():
		name = row[0]
		users.append(name)


	return users




def queryUser(user_id):
	userID = user_id

	query = """SELECT * FROM USER WHERE USER.id = {}""".format(userID)
	try:
		cursor.execute(query)

		for row in cursor.ftechone():
			name = row['name']
			email = row['email']
			phone = row['phone']


			user = {"name":name, "email":email, "phone":phone}


			return user

	except:
		return {"messaege":"user not in db"}





def queryUserEmail(user_email):
	userEmail = user_email

	query = """SELECT name FROM USER WHERE USER.email = {}""".format(userEmail)
	cursor.execute(query)
	count = cursor.fetchone()
	user = count[0]

	if user:
		response = {"user":user}

	else:
		response ="User not found"

	return response




def queryCourses():
	courses = []
	query = """SELECT name FROM COURSE"""
	cursor.execute(query)

	for row in cursor.fetchall():
		course = row[0]
		courses.append(course)


	return courses





def dashboardQuery(email, password):
	mail = email
	passwd = password

	query = """SELECT password, id FROM USER WHERE email = {}""".format(mail)
	cursor.execute(query)
	count = cursor.fetchone()
	count = len(count)

	if count > 0:
		print("User exist")
		password = cursor.fetchone()

		if password == passwd:
			print("Password match")
			response = (True, userID)

		else:
			print("Password mismatch")
			response = (False, userID)


	else:
		print("User do not exist")
		response = (False, userID)


	return response





def verifyImage(file, user_id):
	imgFile = file
	userID = user_id
	data = imghrd.what(imgfile)
	timenow = datetime.now
	timestmp = timenow.time()
	timeFile = str(timestmp.hour)+":"+str(timestmp.minute)+":"+str(timestmp.second)
	randFile = rnadom.randint(1,10)

	timeFile = timeFile + str(randFile)

	if data == 'png' or data == 'jpeg':
		print("Valid File")
		imgfile.filename = str(timeFile)
		imagePath = ""
		try:
			query = """INSERT INTO PAYMENT_DETAILS (user_id,image_path) values({},{})""".format(userID, imagePath)
			cursor.execute(query)
			message = """\
			Subject: Payment Document Uploaded

			Te payment document for user {} has been uploaded succssfuy
			""".format(userID)

			context = ssl.create_default_context()
			with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
				server.login(sender_email, password)
				server.sendmail(sender_email, receiver_email, message)

			response = {"messsage": "document uploaded successfully."}


		except Exception as error:
			response = {"message":"Failed"}


	else:
		print("Invalid File")
		response = False



def confirmAdmin(user_id):
	userID = user_id
	query = """SELECT USER_ROLE.role_id from USER_ROLE INNER JOIN USER ON USER.id=USER_ROLE.user_id WHERE USER.id = '{}'""".format(userID)
	cursor.execute(query)
	count =  cursor.fetchone()
	role_id = count[0]

	if role_id == 'admin':
		response = 'User is admin'
	else:
		response = 'User is not admin'


	return response



def confirmUserPay(user_id):
	userID = user_id
	query = """SELECT * FROM PAYMENT_DETAILS WHERE user_id = {}"""format(userID)
	cursor.execute(query)
	count = cursor.fetchone()

	if len(count) > 0:
		response = "Payment confirmed"

	else:
		response = "No payment"

	return response



def updateCourse(course_id, discount, discount_on, discount_ends):
	courseID = course_id
	disc = discount
	discON = discount_on
	discEND = discount_ends

	query = """UPDATE COURSE SET discount = {}, discount_ends = {}, discont_on = {} WHERE COURSE.id = {}""".format(disc, discEND, discON, courseID)
	try:
		cursor.execute(query)
		response = {"message":"course edited successfully"}

	except Exception as error:
		response = {"message":"course not updated"}




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







def storeCourseObj(syllabus,title,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts):
	query = "INSER INTO COURSE (syllabus,title,name,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts) values ({},{},{},{},{},{},{},{},{})".format(syllabus,title,title,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts)
	try:
		cursor.execute(query)
		return "course created"

	except Exception as error:
		print(error)
		return "course not created"


def updateCourseObj(course_id,syllabus,title,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts):
	query = """UPDATE COURSE SET syllabus = {},title = {}, name = {} ,weekday_price = {},weekday_duration = {},weekday_starts = {},weekend_price = {},weekend_duration = {},weekend_starts = {} WHERE course_id = {}""".format(syllabus,title,title,weekday_price,weekday_duration,weekday_starts,weekend_price,weekend_duration,weekend_starts,course_id)
	try:
		cursor.execute(query)
		return "course edited successfully"

	except Exception as error:
		return "course not edited"


