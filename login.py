from flask import Flask,render_template,url_for,request,session,logging,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
import os

app = Flask(__name__)

engine=create_engine("mysql+pymysql://root:root@localhost/user")	#mysql+pymysql://username:password@localhost/databasename
db=scoped_session(sessionmaker(bind=engine))
app.secret_key=os.urandom(24)


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        confirm=request.form.get("confirm")
        email = request.form.get("email")

        usernamedata=db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()

        if usernamedata==None:
            if password==confirm:
                db.execute("INSERT INTO users(username,password,email) VALUES(:username,:password,:email)",{"username":username,"password":password,"email":email})
                db.commit()
                flash("You are registered and can now login","success")
                return redirect(url_for('login'))
            else:
                flash("Password does not match","danger")
                return render_template('register.html')
        else:
            flash("User already existed, please login or contact admin","danger")
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")

        usernamedata=db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
        passworddata=db.execute("SELECT password FROM users WHERE username=:username",{"username":username}).fetchone()

        #print(type(usernamedata[0]))
        #print(type(passworddata[0]))
        #print(type(username))
        #print(type(password))

        if usernamedata[0] is None:
            "<h1>Not a valid username</h1>"
            return render_template('login.html')
        else:
            if password == passworddata[0]:
                #session["users_id"]=True
                flash("You are now logged in!!","success")
                return redirect(url_for('home')) #Opens welcome screen
            else:
                flash("Incorrect Password","danger")
                return render_template('login.html')

    return render_template('login.html')

@app.route('/home',)
def home():
    return render_template("home.html")


if __name__== "__main__":
    app.run(debug="TRUE")
