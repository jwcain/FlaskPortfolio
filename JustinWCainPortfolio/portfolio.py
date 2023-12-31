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
    project_link_tuple_set = get_project_link_tuple_set()
    return render_template('portfolio/projects.html', project_link_tuple_set=project_link_tuple_set)

@bp.route('/project/create', methods=('GET',))
@login_required
def create_project():
    db = get_db()
    response = db.execute(
        'INSERT INTO project (shown, programming_language, tools_used, title, info, last_updated)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (1, '', '', '', '', '2023-08-01')
    )
    db.commit()

    return redirect(url_for('portfolio.update_project', id=response.lastrowid))

@bp.route('/project/addlink/<int:id>', methods=('post',))
@login_required
def add_link_project(id):
    db = get_db()
    db.execute(
        'INSERT INTO project_link (project_id, title, link)'
        ' VALUES (?, ?, ?)',
        (id, '','')
    )
    db.commit()

    return redirect(url_for('portfolio.update_project', id=id))

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

def get_project_links(id):
    return get_db().execute('SELECT * FROM project_link WHERE project_id = ?' , (id,)).fetchall()

def get_project_link_tuple_set():
    project_link_tuple_set= []
    db = get_db()
    if g.user:
        projects = db.execute(
            'SELECT * FROM project'
        ).fetchall()
    else:
        projects = db.execute(
        'SELECT * FROM project WHERE shown = True'
        ).fetchall()
    for project in projects:
        project_links = get_project_links(project['id'])
        project_link_tuple_set.append((project, project_links))

    return project_link_tuple_set


@bp.route('/project/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update_project(id):
    project = get_project(id)
    project_links = get_project_links(id)
    if request.method == 'POST':
        shown = 'shown' in request.form
        programming_language = request.form['programming_language']
        tools_used = request.form['tools_used']
        title = request.form['title']
        info = request.form['info']
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
                'UPDATE project SET shown = ?, programming_language = ?, tools_used = ?, title = ?, info = ?, last_updated = ?'
                'WHERE id = ?',
                (shown, programming_language, tools_used, title, info, last_updated, id)
            )

            links = get_project_links(id)
            for link in links:
                link_title = request.form['link_{}_title'.format(link['id'])]
                link_link = request.form['link_{}_link'.format(link['id'])]
                db.execute('UPDATE project_link SET title = ?, link = ? WHERE id= ?',
                (link_title, link_link, link['id']))

            db.commit()
            flash('Project Updated')
            return redirect(url_for('portfolio.projects'))

    return render_template('portfolio/project/update.html', project=project,links=project_links)

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

@bp.route('/project/deletelink/<int:project_id>/<int:link_id>', methods=('POST',))
@login_required
def delete_project_link(project_id,link_id):
    db = get_db()
    db.execute('DELETE FROM project_link WHERE id = ?', (link_id,))
    db.commit()
    return redirect(url_for('portfolio.update_project', id=project_id))

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
    recipe = get_db().execute(
        'SELECT *'
        ' FROM recipe'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if recipe is None:
        abort(404, f"Recipe id {id} doesn't exist.")

    return recipe

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


@bp.route('/recipe/show/<int:id>', methods=('GET',))
def show_recipe(id):
    recipe = get_recipe(id)
    contenttuple = get_recipe_contenttuple(id)
    return render_template('portfolio/recipe/show.html', recipe=recipe, step_ingredientlist_pair=contenttuple[0], all_ingredients=contenttuple[1])


@bp.route('/recipe/update/<int:id>', methods=('POST', 'GET'))
@login_required
def update_recipe(id):
    recipe = get_recipe(id)
    if request.method == 'POST':
        db = get_db()
        recipe_title = request.form['title']
        recipe_summary = request.form['summary']
        recipe_info = request.form['info']

        db.execute('UPDATE recipe SET title = ?, summary = ?, info = ? WHERE id= ?',
        (recipe_title, recipe_summary, recipe_info, id))

        steps = db.execute('SELECT * FROM recipe_step WHERE recipe_id = ?', (id,)).fetchall()
        for step in steps:
            step_info = request.form['step_{}'.format(step['id'])]
            db.execute('UPDATE recipe_step SET info = ? WHERE id= ?',
            (step_info, step['id']))

            ingredients = db.execute('SELECT * FROM recipe_ingredient WHERE recipe_id = ? AND step_id = ?', (id, step['id'])).fetchall()
            for ingredient in ingredients:
                substring = 'step_{}_ingredient_{}'.format(step['id'], ingredient['id'])
                ingredient_amount = request.form['{}_{}'.format(substring, 'amount')]
                ingredient_name = request.form['{}_{}'.format(substring, 'name')]
                db.execute('UPDATE recipe_ingredient SET amount = ?, ingredient_name = ? WHERE id= ?',
                (ingredient_amount, ingredient_name , ingredient['id']))

        db.commit()
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
    db.execute('INSERT INTO recipe_ingredient (recipe_id, step_id, amount, ingredient_name) VALUES (?,?,?,?)',
        (recipe_id,step_id,'',''))
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

@bp.route('/recipe/deletestep/<int:recipe_id>/<int:step_id>', methods=('POST',))
@login_required
def delete_recipe_step(recipe_id, step_id):
    get_recipe(recipe_id)
    db = get_db()
    db.execute('DELETE FROM recipe_step WHERE id = ?', (step_id,))
    db.execute('DELETE FROM recipe_ingredient WHERE step_id = ?', (step_id,))
    db.commit()
    return redirect(url_for('portfolio.update_recipe', id=recipe_id))

@bp.route('/recipe/deleteingredient/<int:recipe_id>/<int:ingredient_id>', methods=('POST',))
@login_required
def delete_recipe_ingredient(recipe_id, ingredient_id):
    get_recipe(recipe_id)
    db = get_db()
    db.execute('DELETE FROM recipe_ingredient WHERE id = ?', (ingredient_id,))
    db.commit()
    return redirect(url_for('portfolio.update_recipe', id=recipe_id))