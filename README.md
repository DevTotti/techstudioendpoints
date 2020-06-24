# techstudioendpoints
TechStdio api endpoints written with Flask


Before running the app on the server, change this;

"app.run(debug=True, port = 4567)"


The above line is in api.py file on the last line and should be changed to;


"app.run()"


without the quotes. This is because the port and host for development is specified and needs to be changed to sever-compatible host


To run on the server, have python installed then run;

"pip install -r requirements.txt"

first then run using;

"python api.py"


#NOTE: The database connections credentils has to be changed first



#NOTE: The function for sending email to the admin whenever a user uploads their payment information needs to get the sender email and the receiver email, this needs to be set on line 18, 19 and 20 in queries.py. Also the mail client needs to be set.