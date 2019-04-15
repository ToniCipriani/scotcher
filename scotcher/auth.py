"""Authentication pages"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from scotcher.db import conn_sql

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Check and register new users"""
    if request.method == 'POST':
        db_conn = conn_sql()
        db_cur = db_conn.cursor()
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        else:
            db_cur.execute(
                'SELECT id FROM tb_user WHERE username = %s', (username,)
                )
            user_id = db_cur.fetchone()
            if user_id is not None:
                error = 'User {} is already registered'.format(username)
        if error is None:
            db_cur.execute(
                'INSERT INTO tb_user (username, password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
                )
            db_conn.commit()
            db_cur.close()
            return redirect(url_for('auth.login'))
        db_cur.close()
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Login screen"""
    if request.method == 'POST':
        db_conn = conn_sql()
        db_cur = db_conn.cursor()
        username = request.form['username']
        password = request.form['password']
        error = None
        db_cur.execute(
            'SELECT username,password FROM tb_user WHERE username = %s', (username,)
        )
        user = db_cur.fetchone()
        db_cur.close()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[1], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    """Add user to session"""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db_conn = conn_sql()
        db_cur = db_conn.cursor()
        db_cur.execute(
            'SELECT * FROM tb_user WHERE username = %s', (user_id,)
        )
        g.user = db_cur.fetchone()
        db_cur.close()

@bp.route('/logout')
def logout():
    """Clear current session and log outuser"""
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    """Function for locking screens requiring login"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        """view wrapper"""
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
