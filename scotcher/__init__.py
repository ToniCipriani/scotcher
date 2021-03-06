"""
The flask application package.
"""

import os

from flask import Flask

def create_app(test_config=None):
    """App Factory"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='dbname=scotcher user=sco_dbo password=Talisker10 host=127.0.0.1 port=5432'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import listing
    app.register_blueprint(listing.bp)
    app.add_url_rule('/', endpoint='index')

    return app
