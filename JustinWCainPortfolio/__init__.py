import os

from markupsafe import Markup 
from flask import Flask, send_file, url_for, redirect
from werkzeug.security import check_password_hash, generate_password_hash



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'JustinWCainPortfolio.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import portfolio
    app.register_blueprint(portfolio.bp)
    app.add_url_rule('/', endpoint='index')

    @app.route('/login')
    def login_shorthand():
        return redirect(url_for('auth.login'))

    app.jinja_env.globals['include_raw'] = lambda filename : Markup(app.jinja_loader.get_source(app.jinja_env, filename)[0])
    return app