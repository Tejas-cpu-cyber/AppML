from flask import Flask , render_template , request , redirect , session , url_for
from sqlite3 import *
import pickle

app = Flask(__name__)
app.secret_key = "lessgo"

@app.route("/")
def home():
	if "username" in session:
		return render_template("home.html" , name =session["username"])
	else :
		return redirect( url_for('login') )

@app.route("/login" , methods=["GET" , "POST"])
def login():
	if request.method == "POST" :
		un = request.form["un"]
		pw = request.form["pw"]
		con = None 
		try :
			con = connect("project1.db")
			cursor = con.cursor()
			sql = "select * from user where username='%s' and password='%s'"
			cursor.execute(sql % (un , pw))
			data = cursor.fetchall()
			if len(data) == 0 :
				return render_template("login.html" , msg="invalid login")
			else :
				session['username'] = un
				return redirect( url_for('home') )
		except Exception as e :
			msg = "issue" + str(e)
			return render_template("login.html" , msg=msg )
	else : 
		return render_template("login.html")

@app.route("/signup" , methods=["GET" , "POST"])
def signup():
	if request.method =="POST":
		un = request.form["un"]
		pw1 = request.form["pw1"]
		pw2= request.form["pw2"]
		if pw1 == pw2 :
			con = None 
			try :
				con = connect("project1.db")
				cursor = con.cursor()
				sql = "insert into user values( '%s' , '%s' )"
				con.execute(sql % (un , pw1))
				con.commit()
				return redirect( url_for('login') )
			except Exception as e :
				con.rollback()
				return render_template('signup.html' , msg="user already exist" )
		else : 
			return render_template('signup.html' , msg= "passwords did not match")
	else : 
		return render_template('signup.html')

@app.route("/logout" , methods=["POST"])
def logout():
	session.clear()
	return redirect( url_for('login') )



@app.route("/check" , methods=["POST"])
def check():
	with open("heart.model" , "rb") as f :
		model = pickle.load(f)
	age = float(request.form["age"])
	bp=float(request.form["bp"])
	cholestrol=float(request.form["cho"])
	hr=float(request.form["hr"])
	op=float(request.form["op"])
	gen=request.form["gender"]
	ecg=request.form["ecg"]
	ea =request.form["ea"]
	bs =request.form["bs"]
	print( age , bp , cholestrol , hr , op , gen , ecg , ea , bs )
	sex = 0 
	if gen == "M":
		sex = 1 
	ecgn , ecgst = 0 , 0 
	if ecg == "n" : 
		ecgn = 1
	if ecg == "st" :
		ecgst = 1
	ex_agina = 0 
	if ea == "y" : 
		ex_agina = 1  
	fbs = 0 
	if bs == "y" : 
		fbs = 1  
	d = [[age , bp , cholestrol , fbs , hr , op , sex , ecgn , ecgst , ex_agina ]]
	print(d)
	res = model.predict(d)
	if res == 0 :
		return render_template("negative.html")	
	else : 
		return render_template("positive.html")

@app.route("/back" , methods=["POST"])
def back():
	return render_template("home.html")	
	

if __name__ == "__main__":
	app.run(debug=True)