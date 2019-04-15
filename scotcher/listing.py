"""Main Listing Function"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.exceptions import abort

from scotcher.auth import login_required
from scotcher.db import conn_sql

bp = Blueprint('listing', __name__)

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
    return render_template('listing/index.html', bottles=bottles)


def get_dist_id(distillery):
    """Get distillery ID"""
    dist_code = None
    db_conn = conn_sql()
    db_cur = db_conn.cursor()
    db_cur.execute('SELECT id FROM tb_distillery WHERE name = %s', (distillery,))
    dist_rec = db_cur.fetchone()
    if dist_rec:
        dist_code = dist_rec[0]
    db_cur.close()
    return dist_code

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Add bottle to inventory"""
    if request.method == 'POST':
        error = None
        name = request.form['name']
        distillery = request.form['distillery']
        age = request.form['age']
        abv = request.form['abv']
        notes = request.form['notes']

        dist_code = get_dist_id(distillery)

        if not name:
            error = 'Bottle Name required'
        elif not dist_code:
            error = 'Distillery is blank or not found'
        elif not age:
            error = 'Age Statement required'
        elif not abv:
            error = 'Alcohol By Volume required'
        else:
            db_conn = conn_sql()
            db_cur = db_conn.cursor()

            # Do insert
            db_cur.execute(
                """INSERT INTO public.tb_whisky (name, distillery, age, abv, owner, notes)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (name, dist_code, age, abv, g.user[0], notes,)
            )
            db_conn.commit()
            db_cur.close()
            return redirect(url_for('listing.index'))

        flash(error)

    return render_template('listing/create.html')

def get_bottle(bottle_id, check_owner=True):
    """Get bottle by ID"""
    db_conn = conn_sql()
    db_cur = db_conn.cursor()
    db_cur.execute(
        """SELECT w.id, u.username,
            w.name, d.name AS distillery,
            d.region, d.country, w.age, w.abv,
            w.notes
            FROM tb_whisky w
            JOIN tb_distillery d ON w.distillery = d.id
            JOIN tb_user u ON u.id = w.owner
            WHERE w.id = %s""", (bottle_id,)
    )
    bottle = db_cur.fetchone()
    db_cur.close()

    if bottle is None:
        abort(404, "Bottle ID {0} does not exist,".format(bottle_id))

    if check_owner and bottle[1] != g.user[1]:
        abort(403)

    return bottle

@bp.route('/<int:bottle_id>/update', methods=('GET', 'POST'))
@login_required
def update(bottle_id):
    """Update a bottle in inventory"""
    error = None
    bottle = get_bottle(bottle_id)

    if request.method == 'POST':
        name = request.form['name']
        distillery = request.form['distillery']
        age = request.form['age']
        abv = request.form['abv']
        notes = request.form['notes']

        dist_code = get_dist_id(distillery)

        if not name:
            error = 'Bottle Name required'
        elif not dist_code:
            error = 'Distillery is blank or not found'
        elif not age:
            error = 'Age Statement required'
        elif not abv:
            error = 'Alcohol By Volume required'
        else:
            db_conn = conn_sql()
            db_cur = db_conn.cursor()
            # Do insert
            db_cur.execute(
                """UPDATE tb_whisky
                   SET name = %s,
                   distillery = %s,
                   age = %s,
                   abv = %s,
                   notes = %s
                   WHERE id = %s
                """, (name, dist_code, age, abv, notes, bottle_id,)
            )
            db_conn.commit()
            db_cur.close()
            return redirect(url_for('listing.index'))

        flash(error)

    return render_template('listing/update.html', bottle=bottle)

@bp.route('/<int:bottle_id>/delete', methods=('POST',))
@login_required
def delete(bottle_id):
    """Remove bottle from inventory"""
    get_bottle(bottle_id)
    db_conn = conn_sql()
    db_cur = db_conn.cursor()
    db_cur.execute('DELETE FROM tb_whisky WHERE id = %s', (bottle_id,))
    db_conn.commit()
    db_cur.close()
    return redirect(url_for('listing.index'))
