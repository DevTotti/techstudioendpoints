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


#NOTE: The database connections have to be changed first