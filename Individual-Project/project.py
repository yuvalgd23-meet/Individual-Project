from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
# // For Firebase JS SDK v7.20.0 and later, measurementId is optional
# const firebase
Config = {
"apiKey": "AIzaSyAOq-rTvSKpM77oBZ-TfTmi_8uau2TnF7o",
"authDomain": "project-py-24856.firebaseapp.com",
"databaseURL": "https://project-py-24856-default-rtdb.europe-west1.firebasedatabase.app",
"projectId": "project-py-24856",
"storageBucket": "project-py-24856.appspot.com",
"messagingSenderId": "159860834309",
"appId": "1:159860834309:web:8621f84a6ac694e3ccdc6c",
"measurementId": "G-6999ED4M3K",
"databaseURL":"https://project-py-24856-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] =auth.sign_in_with_email_and_password(email, password)
			
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
	return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		#try:
		login_session['user'] = auth.create_user_with_email_and_password(email, password)
		user = {"name":request.form['full_name'],"username":request.form['username'], "email":request.form['email'],"password":request.form['password'], "bio":request.form['bio'] }
		db.child('Users').child(login_session['user']["localId"]).set(user)
		return redirect(url_for('home'))
		# except:
		# 	error = "Authentication failed"
	return render_template("signup.html")




@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == 'POST':
		try:
			tweet = {"title": request.form['title'],"text": request.form['text']}
			db.child("Tweets").push(tweet)
		except:
			print("Couldn't add tweet")

		return render_template("add_tweet.html")



@app.route('/signout')
def signout():
	login_session['user'] = None
	auth.current_user = None 
	return redirect(url_for('signin'))




# Variables for tasks
image_link = "data:image/png;base64,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"
user_bio = "Foot Locker - 'its about the quality not the price'."

posts = {
"https://www.sheerid.com/shoppers/wp-content/uploads/sites/4/2020/05/deal-page-467x316-footlocker.jpg":"shoes",
    "https://media-exp1.licdn.com/dms/image/C4D1BAQFTbpgMk3KTSg/company-background_10000/0/1614595305396?e=1659178800&v=beta&t=OiSIvxsPJiJkArJIzBCKVF0_-yEta9gv1qLVnViU8bo": "MEET graduation!",
    "https://pbs.twimg.com/media/FPvsO6xVkAEcrBm?format=jpg&name=900x900": "#Throwback to one of our favorite #MEETsummer events: #BowlingNight!",
    "https://pbs.twimg.com/media/FI_UkcnVIAAUvWN?format=jpg&name=medium": "2020 cohort in their Y1 summer!"}


#####


@app.route('/index', methods = ['GET', 'POST'])  # '/' for the default page
def home():
	return render_template('index.html',image_link=image_link, user_bio=user_bio, user1=db.child('Users').child(login_session['user']['localId']).child('username').get().val())
@app.route('/shoes', methods=['GET', 'POST'])
def shoes():
	return render_template('shoes.html')

@app.route('/clothing', methods=['GET', 'POST'])
def clothes():
	return render_template('clothing.html')

@app.route('/kids', methods=['GET', 'POST'])
def kids():
	return render_template('kids.html')

@app.route('/about')  # '/' for the default page
def about():
    return render_template('about.html')


if __name__ == "__main__":  # Makes sure this is the main process
    app.run(debug=True)

