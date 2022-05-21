import os 
from flask import Flask


def (test_config=None):
    #creat and configure the app
        #create an instance of Flask
        #__name__ (name of the current py module, its also the path to it)
        #instance_relative_config=True tells the app that configuration files are relative to the instance folder, which is located outside the flaskr package(should not be commited)

    app = Flask(__name__,instance_relative_config=True) 

    #app.config.from_mapping() sets default configuraation that the app will you
    app.config.from_mapping(
        # SECRECT_KEY used by Flask and extensions to keep data safe.set to dev when in development but should be replaced with random  val when deploying 
        SECRET_KEY = 'dev',
        #DATABASE path to where the SQLlite database file is saved, under the app.instance_path (the path chosen by flask)
        DATABASE = os.path.join(app.instance_path,'flaskr.sqlite'),

    ) 
    if test_config is None:
        #load the instance config, if it exists, when not testing 
            #app.config.from_pyfile overrides default config with values taken from config.py file  in the instance folder if it exists(eg when deploying it can be used to sset a real SECRET_KEY)  
        app.config.from_pyfile('config.py',silent = True)
    else:
        #load the test config if passed in
            #test_config can be passed to the factory,will be used instead of the instance config
        app.config.from_mapping(test_config)
    #ensure the instance folder
    try:
        # os.makedirs ensures that app.instance_path exists(not created automatuically but needs to be ceated, will create the SQLlite file there )
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #a simple page that says hello
        # @app.route() creates a simple route so you can see the application working. it creates a connection between URL /hello and a function that returns a response , the string 'Hello, World!'
    @app.route('/hello')
    def hello():
        return 'Hello, world!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/',endpoint='index')

    return app
