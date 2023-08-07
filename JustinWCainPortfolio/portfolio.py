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

#------------------------------------------------------------------------------ PROJECTS
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

@bp.route('/project/create', methods=('GET', 'POST'))
@login_required
def create_project():
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
        abort(404, f"Project id {id} doesn't exist.")

    return post

@bp.route('/project/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update_project(id):
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
def toggle_project(id):
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
def delete_project(id):
    get_project(id)
    db = get_db()
    db.execute('DELETE FROM project WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('portfolio.projects'))

#-------------------------------------------------------------- Recipes
@bp.route('/recipes')
def recipes():
    db = get_db()
    recipes = db.execute(
    'SELECT * FROM recipe'
    ).fetchall()
    return render_template('portfolio/recipes.html', recipes=recipes)

@bp.route('/recipe/create/')
@login_required
def create_recipe():
    db = get_db()
    response = db.execute(
        'INSERT INTO recipe (title, summary, info)'
        ' VALUES (?, ?, ?)',
        ('','','')
    )
    db.commit()
    return redirect(url_for('portfolio.update_recipe', id=response.lastrowid))

def get_recipe(id):
    post = get_db().execute(
        'SELECT *'
        ' FROM recipe'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Recipe id {id} doesn't exist.")

    return post

def get_recipe_contenttuple(recipe_id):
    step_ingredientlist_pair = []
    all_ingredients = []
    db = get_db()
    steps = db.execute('SELECT * FROM recipe_step WHERE recipe_id = ?' , (recipe_id,)).fetchall()
    for step in steps:
        ingredients = db.execute('SELECT * FROM recipe_ingredient WHERE recipe_id = ? AND step_id = ?' , (recipe_id, step['id'])).fetchall()
        step_ingredientlist_pair.append((step, ingredients))
        for ingredient in ingredients:
            all_ingredients.append(ingredient)
    return (step_ingredientlist_pair, all_ingredients)


@bp.route('/recipe/update/<int:id>')
@login_required
def update_recipe(id):
    recipe = get_recipe(id)
    if request.method == 'POST':
        #TODO: Handle post
        return redirect(url_for('portfolio.recipes'))
    contenttuple = get_recipe_contenttuple(id)
    return render_template('portfolio/recipe/update.html', recipe=recipe, step_ingredientlist_pair=contenttuple[0], all_ingredients=contenttuple[1])

@bp.route('/recipe/addstep/<int:id>', methods=('POST',))
@login_required
def addstep_recipe(id):
    db = get_db()
    response = db.execute('SELECT * FROM recipe_step WHERE id = ?', (id,)).fetchall()
    db.execute('INSERT INTO recipe_step (recipe_id, step_order, info) VALUES (?,?,?)',
        (id,len(response)+1,''))
    db.commit()
    return redirect(url_for('portfolio.update_recipe', id=id))

@bp.route('/recipe/step/addingredient/<int:recipe_id>/<int:step_id>', methods=('POST',))
@login_required
def addingredient_step_recipe(recipe_id, step_id):
    db = get_db()
    db.execute('INSERT INTO recipe_ingredient (recipe_id, step_id, info) VALUES (?,?,?)',
        (recipe_id,step_id,''))
    db.commit()
    return redirect(url_for('portfolio.update_recipe', id=recipe_id))

@bp.route('/recipe/delete/<int:id>', methods=('POST',))
@login_required
def delete_recipe(id):
    get_recipe(id)
    db = get_db()
    db.execute('DELETE FROM recipe WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('portfolio.recipes'))