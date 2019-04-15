"""Main Listing Function"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.exceptions import abort

from scotcher.auth import login_required
from scotcher.db import conn_sql

bp = Blueprint('listing',__name__)

@bp.route('/')
def index():
    """Main Index Page, lists all available bottles"""
    db_conn = conn_sql()
    db_cur = db_conn.cursor()
    db_cur.execute(
        """SELECT w.id, u.username,
            w.name, d.name AS distillery,
            d.region, d.country, w.age, w.abv,
            w.notes
            FROM tb_whisky w
            JOIN tb_distillery d ON w.distillery = d.id
            JOIN tb_user u ON u.id = w.owner"""
    )
    bottles = db_cur.fetchall()
    db_cur.close()
    return render_template('listing/index.html',bottles=bottles)
