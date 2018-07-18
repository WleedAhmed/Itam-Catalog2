from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   jsonify,
                   url_for,
                   flash)
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Movie, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Filmography"

# connect to DB
engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current'
                                            ' user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-rad' \
              'ius: 150px;-webkit-border-radius: 150px;-moz-border-' \
              'radius: 150px;"> '
    flash("you are now logged in %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(
        User).filter_by(email=login_session['email']).one_or_none()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one_or_none()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON endpoints
@app.route('/category/<int:category_id>/movie/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one_or_none()
    movies = session.query(Movie).filter_by(
        category_id=category_id).all()
    return jsonify(Movies=[i.serialize for i in movies])


@app.route('/category/<int:category_id>/movie/<int:movie_id>/JSON')
def MovieJSON(category_id, movie_id):
    Movie_ = session.query(Movie).filter_by(id=movie_id).one_or_none()
    return jsonify(Movie_=Movie_.serialize)


@app.route('/category/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# Show all categories
@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).all()
    # editt
    allmovies = session.query(Movie).order_by(desc(Movie.id)).all()
    # return "This page will show all my categories"
    if 'username' not in login_session:
        return render_template('publiccategories.html',
                               categories=categories, allmovies=allmovies)
    else:
        return render_template('categories.html', categories=categories,
                               allmovies=allmovies)


# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        if newCategory.name:
            session.add(newCategory)
            flash('New Category %s Successfully Created' % newCategory.name)
            session.commit()
            return redirect(url_for('showCategories'))
        else:
            flash('You should add a name for the new category. Nothing added.')
            return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')
    # return "This page will be for making a new category"


# Edit a category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(
        Category).filter_by(id=category_id).one_or_none()
    if 'username' not in login_session:
        return redirect('/login')
    if editedCategory.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are" \
               " not authorized to edit this category. Please" \
               " create your own category in order" \
               " to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategories'))
    else:
        return render_template(
            'editCategory.html', category=editedCategory)

    # return 'This page will be for editing category %s' % category_id


# Delete a category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one_or_none()
    if 'username' not in login_session:
        return redirect('/login')
    if categoryToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not" \
               " authorized to delete this" \
               " category. Please create your own category in order to" \
               " delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(
            url_for('showCategories', category_id=category_id))
    else:
        return render_template(
            'deleteCategory.html', category=categoryToDelete)
    # return 'This page will be for deleting category %s' % category_id


# Show category's movies
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/movie/')
def showMovie(category_id):
    category = session.query(Category).filter_by(id=category_id).one_or_none()
    movies = session.query(Movie).filter_by(category_id=category_id).all()
    creator = getUserInfo(category.user_id)
    if 'username' not in login_session or \
            creator.id != login_session['user_id']:
        return render_template('publicmovie.html', movies=movies,
                               category=category, creator=creator)
    else:
        return render_template('movie.html', movies=movies, category=category)

    # return 'This page is the movie for category %s' % category_id


# Create a new movie
@app.route(
    '/category/<int:category_id>/movie/new/', methods=['GET', 'POST'])
def newMovie(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one_or_none()
    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {alert('You" \
               " are not authorized to add movie" \
               "s in this catego" \
               "ry. Please create your own category in o" \
               "rder to add movies.');}</scr" \
               "ipt><body onload='myFunction()'>"
    if request.method == 'POST':
        newMovie = Movie(name=request.form['name'], description=request.form[
                           'description'], category_id=category_id)
        if newMovie.name:
            session.add(newMovie)
            session.commit()
            flash('New movie %s successfully created' % (newMovie.name))
        else:
            flash('You should add a name for the new movie. Nothing added.')
        return redirect(url_for('showMovie', category_id=category_id))
    else:
        return render_template('newMovie.html', category_id=category_id)

    return render_template('newMovie.html', category=category)
    # return 'This page is for making a new movie for category %s'
    # %category_id


# Edit a movie
@app.route('/category/<int:category_id>/movie/<int:movie_id>/edit',
           methods=['GET', 'POST'])
def editMovie(category_id, movie_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedMovie = session.query(Movie).filter_by(id=movie_id).one_or_none()
    category = session.query(Category).filter_by(id=category_id).one_or_none()
    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {alert('You " \
               "are not authorized to edit" \
               " movies in this category. Please create " \
               "your own category in order to edit movi" \
               "es.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedMovie.name = request.form['name']
        if request.form['description']:
            editedMovie.description = request.form['description']
        session.add(editedMovie)
        session.commit()
        flash('Movie Successfully Edited')
        return redirect(url_for('showMovie', category_id=category_id))
    else:

        return render_template(
            'editmovie.html', category_id=category_id, movie_id=movie_id,
            item=editedMovie)

    # return 'This page is for editing movie %s' % movie_id


# Delete a movie
@app.route('/category/<int:category_id>/movie/<int:movie_id>/delete',
           methods=['GET', 'POST'])
def deleteMovie(category_id, movie_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one_or_none()
    movieToDelete = session.query(Movie).filter_by(id=movie_id).one_or_none()
    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {alert('You" \
               " are not authorized t" \
               "o delete movies in this category. Please create your own" \
               " category in order to delete movies" \
               ".');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(movieToDelete)
        session.commit()
        flash('Movie Successfully Deleted')
        return redirect(url_for('showMovie', category_id=category_id))
    else:
        return render_template('deletemovie.html', item=movieToDelete)
    # return "This page is for deleting movie %s" % movie_id


# editt
# show specific movie
@app.route('/category/<int:category_id>/movie/<int:movie_id>')
def showoneMovie(category_id, movie_id):
    category = session.query(Category).filter_by(id=category_id).one_or_none()
    movie = session.query(Movie).filter_by(
        id=movie_id, category_id=category_id).one_or_none()
    creator = getUserInfo(category.user_id)
    if movie:
        if 'username' in login_session and \
                creator.id == login_session['user_id']:

            return render_template('one_movie.html', movie=movie,
                                   category=category, creator=creator)
        else:
            return render_template('public_one_movie.html', movie=movie,
                                   category=category)
    else:
        return "invalid adress"


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        gdisconnect()
        del login_session['gplus_id']
        del login_session['access_token']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
