import sqlite3

import pytest
from JustinWCainPortfolio.db import get_db, init_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

def test_init_admin_command(runner, app):
    with app.app_context():
        init_db()
        db = get_db()
        result = db.execute('SELECT * FROM user').fetchall()
        assert len(result) == 0
        runner.invoke(args=['init-admin', 'adminpass'])
        result = db.execute('SELECT * FROM user').fetchall()
        assert len(result) == 1


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('JustinWCainPortfolio.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called