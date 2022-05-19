from mimetypes import init
import sqlite3
from webbrowser import get
import click
import dbus
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
     #g is a special object and is unique for each request. 
     # USed to store data can be accessed by multiple functions during the request. 
     # the connection is stored and reused instead of creating a new connection if get_db is called a second 
     #      time in the same request. 

    if 'db' not in g:
            #sqlite3.connect() establish a connection to the file poinnted to at the DATABASE configuration key(doesnt exist yet until initialize the db)
        g.db=sqlite3.connect(
            #current_app (special object)Points to the Flask app handling the request
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
                    #sqlite3.Row tells the connection to return rows that behave like dicts, this allows accessing the column by name
        g.db.row_factory=sqlite3.Row
    return g.db
def close_db(e=None):
    db=g.pop('db',None)

    if db is not None:

        #checks if a connection was created by checking if g.db was set,if the connection exists, it is closed
        db.close()

"""Add the Python functions that will run these SQL commands to the db.py"""
def init_db():
    db=get_db()
    #open_resource() opens a file relative to the flaskr package. it is necessary because you won't know where that location is when deploying the application 
    # (get_db returns a database connection, which is used to execute the commands reader from the file) 
    with current_app.open_resource('schema.sql') as f:
       # print(f.read().decode('utf8'))
        db.executescript(f.read().decode('utf8'))

#click.command() defines a command line command called init_db that calls the init_db function and shows a success message to the user
@click.command('init_db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('intialized the database')

"""Register with the Application"""
def init_app(app):
    # app.teardown_appcontext() tells flask to call that function when cleaning up after returning the response 
    app.teardown_appcontext(close_db)
    #app.cli.add_command() adds a new command that can be called with the flask command 
    app.cli.add_command(init_db_command)
