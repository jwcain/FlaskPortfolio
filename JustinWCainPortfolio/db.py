import sqlite3

import click
from flask import current_app, g
from werkzeug.security import generate_password_hash


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_admin_command)

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('init-admin')
@click.argument('password')
def init_admin_command(password):
    """Adds admin with hashed password."""
    db = get_db()
    db.execute(
        "INSERT INTO user (username, password) VALUES (?, ?)",
        ('admin', generate_password_hash(password)),
    )
    db.commit()
    click.echo('Initialized the admin.')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()