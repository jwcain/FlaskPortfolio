from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from JustinWCainPortfolio.auth import login_required
from JustinWCainPortfolio.db import get_db

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    db = get_db()

    return render_template('index.html')