from flask import Flask, request, jsonify, render_template, url_for
from flask_mail import *  
import sys
import threading
	
try:
	kwar = sys.argv[1].split('=')
	kwar = {kwar[0]:kwar[1]} 
	if kwar['module_version'] == "v3":
		from evaluation_models.cannyeval_v3 import *
	else:
		from evaluation_models.cannyeval_v1 import *
except :
	from evaluation_models.cannyeval_v1 import *
app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'pranuthota31@gmail.com'  
app.config['MAIL_PASSWORD'] = '$%6&*yhn'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  
mail = Mail(app)
SEND_MAIL_TO = app.config['MAIL_USERNAME']
UPLOADS_DIR = r"C:\Users\T.PRANEETH\Desktop\ML Workshop\My_Startup_Ideas\Canny.ai"

@app.route('/test')
def juss_testing():
	return "Juss Testing"
def input_file():
	return render_template('input_file.html', title="page", jsonfile=json.dumps(data))	
@app.route('/gradeit', methods=["POST"])
def grade():
	global SEND_MAIL_TO
	global UPLOADS_DIR
	
	input_form = request.form
	file = request.files['data json']
	
    		
	evaluator = CannyEval()
    		
	try:
		if file.filename != '':
			data_json = json.load(file)
			
		else:
			data_json = json.load(open(input_form['data json']))
    			
    			
		SEND_MAIL_TO = input_form["mail id"]
	except Exception as e:
		print(e)
		return "SOME ERROR IN APPLICATION"
	report = evaluator.report_card(data_json=data_json, max_marks=int(input_form['max marks']), relative_marking=eval(input_form['relative marking']), integer_marking=eval(input_form['integer marking']), json_load_version="v2")
	if type(report) == AssertionError:
		return "Incompatible Json Format"
	dictToReturn= report.to_json()
	csvToMail = report.to_csv(r"C:\Users\T.PRANEETH\Desktop\ML Workshop\My_Startup_Ideas\Canny.ai\userfiles\report.csv")
	resp = mail_results() #json.loads(dictToReturn)
	return resp
		    
	
#return "We have started to evaluate, seems like it's gonna take some time, we don't want you to just stare at the screen and waste your day, consider this job is done we shall notify you of it's status soon"
	

	
	
@app.route('/')
def home():
	return render_template('home_alt.html')
def mail_results():
	global SEND_MAIL_TO
	global UPLOADS_DIR
	msg = Message("!!We Are Done Evaluating Your Students' Answers!!", sender = 'pranuthota31@gmail.com', recipients=[SEND_MAIL_TO])  
	msg.body = "Greetings from Canny.works,\n\n\tWe took a look into your students' answer sheets and graded them as cannily as possible. Go on and check for yourself if the time you invested in contacting us was worth it or not. Report in the attachment.\n\n\tDon't forget to feed us back with your comments or compliments\n\nRegards,\nCannyTeam " 
	with app.open_resource(r"C:\Users\T.PRANEETH\Desktop\ML Workshop\My_Startup_Ideas\Canny.ai\userfiles\report.csv") as fp:  
		msg.attach("report.csv","text/csv",fp.read())
		mail.send(msg) 
	return render_template('end_card_alt.html')

if __name__ == "__main__":
	

	app.run(host="127.0.0.1", debug=True)