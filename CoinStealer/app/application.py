import os
import helpers
import models
import json
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify, abort, Response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import RegisterForm, ChangePasswordForm
from flask_migrate import Migrate
from database import init_db, db_session

"""
Flask Config
"""
app = Flask(__name__)
app.config['DEBUG'] = False
app.secret_key="somethingsometwhign"

FLAG = "evlz{d0nt_exp0s3_y0uR_api_k3ys}ctf"
FLAG_COST = 10000

migrate = Migrate(app, db_session)
# Prevent caching
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.context_processor
def inject_user(): # Inject user data for the layout in every page
    return dict(user=current_user)

"""
    Flask-Login Config
"""
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return models.User.query.filter_by(username = username).first()

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("login",next=request.endpoint))

"""
    API ROUTES
"""

@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        form = RegisterForm()
        return render_template("index.html", form=form, flag_cost=FLAG_COST)

@app.route("/wallet")
@login_required
def wallet():
    if request.method == "GET":
        return render_template('wallet.html', wallet=current_user.wallet)

@app.route("/transactions", methods=['GET'])
@login_required
def transactions():
    if request.method == "GET":
        transactions = models.Transaction.query.all()
        
        return render_template("transactions.html", transactions = transactions)
@app.route("/transaction/<uuid>", methods=["GET", "PATCH"])
@login_required
def transaction(uuid = None):
    if request.method == 'GET':
        if uuid is None:
            abort(404)
        
        transaction = models.Transaction.query.get(uuid)
        if not transaction:
            abort(404)
        return render_template('transaction.html', transaction = transaction)

    elif request.method == "PATCH":
        if not request.args.get("APIKEY") == 'a3e419378b514f2db99c4d00a1a5fcd9':
            return jsonify({"error": "Incorrect APIKEY"})

        if uuid is None:
            return jsonify({"error": "UUID Not Found"})    

        transaction = models.Transaction.query.get(uuid)
        if not transaction:
            return jsonify({"error": "No Transaction Found"})

        if not request.mimetype == 'application/json':
            return jsonify({"error": "Incorrect Content-Type"})

        if request.get_json():
            updateData = request.get_json()
        else:
            return jsonify({"error": "Invalid Payload"})
        
        signatures = []

        if 'signatures' in updateData:
            for signature in updateData['signatures']:
                signatures.append(models.TransactionSignature(signature))
        
        transaction.signatures = signatures
        db_session.commit()

        return jsonify({'sucess' : True})


        
@app.route("/buyflag", methods=['GET'])
@login_required
def buy_flag():
    if request.method == "GET":
        if current_user.wallet.value >= FLAG_COST:
            return render_template("flag.html", flag=FLAG)
        else:
            return render_template("flag.html", flag='No Flag For The Broke, Go Patch Yourself Up')


"""
    AUTH ROUTES

"""

"""
/register
template - register.html
"""
@app.route("/register", methods=["GET","POST"])
def register():
  form = RegisterForm()
  if request.method == "GET":
    return render_template("register.html",form = form)
  elif request.method == "POST":
    if form.validate_on_submit():
        if models.User.query.get(form.username.data):
            try:
                user = models.User.query.get(form.username.data)
            except :
                db_session.rollback()
                return render_template("register.html", form=form, message="Error Ocurred")
            if form.password.data == user.password:
                login_user(user)
                return redirect(url_for("index"))
            else:
                return render_template("register.html", form=form, message="User Already Exists!")
        else:
            newUser = models.User(username=form.username.data, password=form.password.data)
            app.logger.debug("New User: "+str(newUser))
            db_session.add(newUser)
            db_session.commit()

            login_user(newUser, remember=True)

            return redirect(url_for("index"))
    else:
      abort(404)

"""
/login
template - login.html
"""
@app.route("/login", methods=["GET","POST"])
def login():
  form = RegisterForm()

  if request.method == 'GET':
      return render_template('login.html', form=form)
  elif request.method == 'POST':
    if form.validate_on_submit():
        try:
            user = models.User.query.get(form.username.data)
        except:
            db_session.rollback()
            return render_template("login.html", form=form, message="Error Ocurred")
        if user:
            if user.password == form.password.data:
                # correct username+password
                app.logger.debug("Logging in User: "+str(user))
                login_user(user, remember=True)
                dest = request.args.get('next')
                try:
                    dest_url = url_for(dest)
                except:
                    return redirect(url_for("index"))
                return redirect(dest_url)
            else:
                # incorrect password
                return render_template("login.html", form=form, message="Incorrect Password!")
        else:
            # user dosen't exist
            return render_template("login.html", form=form, message="Incorrect Username or User Dosen't Exist!")
    else:
        return render_template("login.html", form=form, message="Invalid Input!")


"""
/logout
"""
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

"""
/change
Change passwords
"""
@app.route("/change", methods=["GET","POST"])
@login_required
def change():
  form = ChangePasswordForm()

  if request.method == "GET":
    return render_template("change.html", form=form)

  elif request.method == "POST":
    oldPass = form.oldpassword.data
    newPass = form.newpassword.data
    newPassReType = form.newpasswordretype.data
    if form.validate_on_submit():
      # Return error if no input is received
      if oldPass is None or newPass is None or newPassReType is None:
        return render_template("change.html",form=form, message="Invalid Input")
      
      # Return error if oldPass dosen't match DB pass
      if not current_user.password == oldPass:
        return render_template("change.html",form=form, message="Incorrect Password")
      
      # Return error if newPass and newPassReType dosen't match
      if not newPass == newPassReType:
        return render_template("change.html",form=form, message="Incorrect Input: Passwords not matching")
  
      current_user.password = newPass
      db_session.commit()
      return render_template("change.html",form=form, message="Password Changed")  

    else:
      return render_template("change.html", form=form, message="Invalid Input")  



if __name__ == '__main__':
    init_db()
    # Heroku has a DATABASE_URL environment var for the Database URL
    if os.environ.get('DATABASE_URL') is not None:
        app.run(host='0.0.0.0', port=80)
    else:
        app.run(host='0.0.0.0', port=5000)