from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from JustinWCainPortfolio.auth import login_required
from JustinWCainPortfolio.db import get_db

bp = Blueprint('portfolio', __name__)


@bp.route('/')
def index():
    db = get_db()

    return render_template('portfolio/index.html')

@bp.route('/resume')
def resume():
    return redirect(url_for('static', filename='JustinWCain_Resume.pdf'))

@bp.route('/projects')
def projects():
    db = get_db()
    if g.user:
        projects = db.execute(
            'SELECT * FROM project'
        ).fetchall()
    else:
        projects = db.execute(
        'SELECT * FROM project WHERE shown = True'
        ).fetchall()
    return render_template('portfolio/projects.html', projects=projects)

@bp.route('/recipes')
def recipes():
    return render_template('portfolio/recipes.html')

@bp.route('/project/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        shown = request.form['shown']
        programming_language = request.form['programming_language']
        tools_used = request.form['tools_used']
        title = request.form['title']
        info = request.form['info']
        link_github = request.form['link_github']
        link_live = request.form['link_live']
        last_updated = request.form['last_updated']
        error = None

        if not title:
            error = 'Title is required.'
        elif not info:
            error = 'Project Info is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO project (shown, programming_language, tools_used, title, info, link_github, link_live, last_updated)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (shown, programming_language, tools_used, title, info, link_github, link_live, last_updated)
            )
            db.commit()
            flash('Project Added!')
            return redirect(url_for('portfolio.projects'))

    return render_template('portfolio/project/create.html')

def get_project(id):
    post = get_db().execute(
        'SELECT *'
        ' FROM project'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return post

@bp.route('/project/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    project = get_project(id)
    if request.method == 'POST':
        shown = 'shown' in request.form
        programming_language = request.form['programming_language']
        tools_used = request.form['tools_used']
        title = request.form['title']
        info = request.form['info']
        link_github = request.form['link_github']
        link_live = request.form['link_live']
        last_updated = request.form['last_updated']
        error = None

        if not title:
            error = 'Title is required.'
        elif not info:
            error = 'Project Info is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE project SET shown = ?, programming_language = ?, tools_used = ?, title = ?, info = ?, link_github = ?, link_live = ?, last_updated = ?'
                'WHERE id = ?',
                (shown, programming_language, tools_used, title, info, link_github, link_live, last_updated, id)
            )
            db.commit()
            flash('Project Updated')
            return redirect(url_for('portfolio.projects'))

    return render_template('portfolio/project/update.html', project=project)

@bp.route('/project/toggle/<int:id>')
@login_required
def toggle(id):
    db = get_db()
    project = get_project(id)
    shown = project['shown']
    db.execute(
        'UPDATE project SET shown = ? WHERE id = ?',
        (not shown, id)
    )
    db.commit()
    flash('Project ' + ('Shown' if not shown else 'Hidden'))
    return redirect(url_for('portfolio.projects'))

@bp.route('/project/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    get_project(id)
    db = get_db()
    db.execute('DELETE FROM project WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('portfolio.projects'))