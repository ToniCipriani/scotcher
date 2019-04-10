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

    @app.route('/hello')
    def hello():
        """Main Page"""
        sql_str = "SELECT w.name, d.name AS distillery, d.region, d.country, w.age, w.abv, w.notes FROM tb_whisky w JOIN tb_distillery d ON w.distillery = d.id"
        bottles = db.exec_sql(sql_str)
        return str(bottles)

    return app
