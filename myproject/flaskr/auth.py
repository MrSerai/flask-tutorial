from crypt import methods
from dbm.dumb import error
import functools
from sqlite3 import IntegrityError

from flask import(
    Blueprint,flash,g,redirect,render_template,request,session,url_for
)
from werkzeug.security import check_password_hash,generate_password_hash
from flaskr.db import get_db

#the line below. Blueprint named 'auth'.
#the Blueprint needs to know where its defined so '__name__ is passed as the second argument.
# The url_prefix will be prepended to all the URLS associated with the blueprint
bp=Blueprint('auth',__name__,url_prefix='/auth')

"""
when navigated to /auuth/register URL, the regisyer view will return HTML with a form for them to fill out. 
when the form is submited, it will validate their input and either show the form again with an error message or create the new user
"""
#@bp.route() associates the URL /register with the register view function. 
#when flask receives a request to /auth/register, it will register view and use the return as the response
@bp.route('/register',methods=('GET','POST'))
def register():
        #if the user submitted the form. request.method will be 'POST'
        #in this case start validating the input
    if request.method=='POST':
        #equest.form[] MAPS the user's entered values on from the form
        username=request.form['username']
        password=request.form['password']
        db=get_db()
        error=None

        if not username:
            error='Username is Required.'
        elif not password:
            error='Password is required'

        if error is None:
            try:
                # print("inside the try")
                #if validation succeeds db.execute takes a SQL query with ? placeholders for any user user inputs 
                db.execute(
                "INSERT INTO user (username,password) VALUES (?,?)",
                (username,generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error=f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method=='POST':
        username= request.form['username']
        password=request.form['password']
        db=get_db()
        error=None
        user=db.execute(
            'SELECT * FROM user WHERE username=?',(username,)
        ).fetchone()
        if user is None:
            error='Incorrect username'
        elif not check_password_hash(user['password'],password):
            error='Incorrect password'
        
        if error is None:
            session.clear()
            session['user_id']=user['id']
            
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id=session.get('user_id')

    if user_id is None:
        g.user=None
    else:
        g.user=get_db().execute(
            'SELECT * FROM user WHERE id=?',(user_id,)
        ).fetchone
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
