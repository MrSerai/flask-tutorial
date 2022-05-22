from ast import Return
from crypt import methods

#from turtle import title
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort 
from flaskr.auth import login_required
from flaskr.db import get_db

bp=Blueprint('blog',__name__)
#The index view should display information about the post that was added 
@bp.route('/')
def index():
    #The index view should display information about the post that was added 
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
        ).fetchall()
    return render_template('blog/index.html',posts = posts)

@bp.route('/create',methods = ('GET','POST'))
@login_required
def create():
    #The create and update views should render and return a 200 OK status for a GET request. 
    #When valid data is sent in a POST request, create should insert the new post data into the database, and update should modify the existing data. 
    #Both pages should show an error message on invalid data.

    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'title is required'
        if error is not None:
            flash(error)
          
        else:
            db = get_db()
            print("Text here", g.user['id'])
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                'values (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')
#"""Update"""
def get_post(id,check_author=True):
    post= get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404,f"Post id {id} doesnt exist.")
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post

@bp.route('/<int:id>/update',methods = ('GET','POST'))
@login_required
def update(id):
    #The create and update views should render and return a 200 OK status for a GET request. 
    # When valid data is sent in a POST request, create should insert the new post data into the database, and update should modify the existing data. 
    # Both pages should show an error message on invalid data.
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'title is required'

        if error is not None:
            flash(error)
        else:
            db=get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title,body,id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html',post = post)
"""Delete"""        
@bp.route('/<int:id>/delete', methods = ('POST',))
@login_required
def delete(id):
    #The delete view should redirect to the index URL and the post should no longer exist in the database.
    get_post(id)
    db=get_db()
    db.execute('DELETE FROM post WHERE id = ?',(id,))
    db.commit()
    return redirect(url_for('blog.index'))
    