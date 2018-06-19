import os
import helpers
import models
import json
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify, abort, Response, make_response, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import RegisterForm, ChangePasswordForm
from database import init_db, db_session

"""
Flask Config
"""
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['DEBUG'] = False
app.secret_key="somethingsomethign"

@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

FLAG = "evlz{aes_des_xor_hex}ctf"
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
        if not current_user.is_authenticated:
            return render_template("index.html")

        response = make_response(render_template('index.html'))

        if not request.cookies.get("test"):
            cookie = helpers.generateCookie(current_user.username, current_user.admin)
            response.set_cookie('test', cookie)
        
        return response

@app.route("/admin", methods=['GET'])
@login_required
def admin():
    if request.method == "GET":
        if not request.cookies.get("test"):
            return redirect(url_for("index"))
        
        cookie = request.cookies.get("test")
        cookie_data = helpers.decryptCookie(cookie)
        return render_template("flag.html", flag=FLAG, adminFlag=cookie_data['admin'])

@app.route("/encryptcookie", methods=["GET"])
def aespt():
    if request.method == "GET":
        if not request.args.get("plaintext"):
            return jsonify({"message": "128bit AES"})

        plaintext = request.args.get("plaintext")
        try:
            ciphertext = helpers.encrypt(plaintext)
            return jsonify({"ciphertext": ciphertext})
        except:
            return jsonify({'error': "Invalid Input"})
        


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
        if models.User.query.filter_by(username=form.username.data).first():
            user = models.User.query.filter_by(username=form.username.data).first()
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
        user = models.User.query.filter_by(username=form.username.data).first()
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
