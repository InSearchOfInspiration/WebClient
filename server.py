from flask import Flask, Response, redirect, url_for, request, session, abort
from flask import render_template
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user, current_user
from request_manager import ConnectionManager

app = Flask(__name__)

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):

    def __init__(self, username, password, token):
        self.name = username
        self.password = password
        self.token = token
        
    def __repr__(self):
        return "%s/%s" % (self.name, self.password)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        print(session['events'])
        return render_template("index.html", events=session['events'])
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        a_session = ConnectionManager(username, password)     
        if a_session.authorize():
            token = a_session.get_token()
            # user = User(username, password, token)
            session['logged_in'] = True
            session['events'] = a_session.get_events()
            return redirect('')
        else:
            return render_template('login.html', error='wrong pass')
    else:
        return render_template('login.html', error=None)
    return home()

# some protected url
# @app.route('/')
# @login_required
# def home():
#     a_name = current_user.name
#     return render_template("index.html", name=a_name)

 
# somewhere to login
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']   
#         a_session = ConnectionManager(username, password)     
#         if a_session.authorize():
#             token = a_session.get_token()
#             user = User(username, password, token)
#             login_user(user)
#             return redirect('')
#         else:
#             return render_template('login.html', error='wrong pass')
#     else:
#         return render_template('login.html', error=None)


# somewhere to logout
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(id)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
