import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from JustinWCainPortfolio.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view



@bp.route('/changepassword', methods=('GET', 'POST'))
@login_required
def changepassword():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        db = get_db()
        error = None
        code = 200
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', ('admin',)
        ).fetchone()

        if not check_password_hash(user['password'], current_password):
            code = 401
            error = 'Incorrect password.'
        elif not new_password.__eq__(confirm_password):
            code = 400
            error = 'New passwords do not match.'

        if error is None:
            code = 200
            db.execute(
            'UPDATE user SET password = ? WHERE id = ?', (generate_password_hash(new_password), user['id'])
            )
            db.commit()
            #Unsure if this double check is necessary, but it helped with debugging
            #user = db.execute(
            #'SELECT * FROM user WHERE username = ?', ('admin',)
            #).fetchone()
            #if not check_password_hash(user['password'], new_password):
            #    error = 'Failed to update password'
            #else:
            flash('Password changed successfully.')
            return redirect(url_for('index')), code

        flash(error)

    return render_template('auth/changepassword.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', ('admin',)
        ).fetchone()

        if not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

