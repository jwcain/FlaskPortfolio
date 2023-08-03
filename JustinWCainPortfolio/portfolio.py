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