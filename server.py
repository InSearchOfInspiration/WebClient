from flask import Flask, Response, redirect, url_for, request, session, abort
from flask import render_template
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user, current_user
from request_manager import ConnectionManager

from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__)
GoogleMaps(app)

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

icons = ['web', 'today', 'textsms', 'perm_media', 'picture_in_picture', 'assignment']


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

        
        a_session = ConnectionManager(session['username'], session['password'], session['token'])
        # session['events'] = a_session.get_events()
        event_list = []
        session['categories'] = []
        for event in a_session.get_events():
            event['icon'] = icons[3]
            event_list.append(event)
        session['events'] = event_list
        for category in a_session.get_categories():
            category['icon'] = icons[a_session.get_categories().index(category) % 6]
            session['categories'].append(category)
        session['locations'] = a_session.get_locations()
        new_list = []
        for location_ in session['locations']:
            new_location = {}
            new_location['lat'] = location_['latitude']
            new_location['lng'] = location_['longitude']
            new_location['icon'] = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
            new_location['infobox'] = '<b>' + location_['date'] + '</b>'
            new_list.append(new_location)

        sndmap = Map(
            identifier="sndmap",
            lat=50.4419,
            lng=30.4419,
            markers=new_list,
            # style='map'
        )

        return render_template("index.html", token=session['token'], events=session['events'], categories=session['categories'], sndmap=sndmap)
 
# @app.route('/add_event/<name>')
# def add_event(name):
#     if not session.get('logged_in'):
#         return redirect(url_for('login'))
#     else:
#         print(name)
#         a_session = ConnectionManager(session['username'], session['password'], session['token'])
#         session['events'] = a_session.get_events()
#         session['categories'] = a_session.get_categories()

        return render_template("index.html", token=session['token'], events=session['events'], categories=session['categories'])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        a_session = ConnectionManager(username, password, '')
        if a_session.authorize():
            token = a_session.get_token()
            session['username'] = username
            session['password'] = password
            session['token'] = token
            # user = User(username, password, token)
            session['logged_in'] = True
            # session['events'] = a_session.get_events()
            # print(session['events'])
            # session['categories'] = a_session.get_categories()
            # print(session['categories'])
            # session['locations'] = a_session.get_locations()
            # print(session['locations'])
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
    session['categories'] = []
    session['events'] = []
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
