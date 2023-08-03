from JustinWCainPortfolio.db import get_db
import re

def test_resume(client):
    response = client.get('/resume', follow_redirects=True)
    assert response.status == '200 OK'

def test_projects(client):
    response = client.get('/projects', follow_redirects=True)
    assert response.status == '200 OK'

def test_admin_projects(client, auth):
    auth.login()
    response = client.get('/projects', follow_redirects=True)
    assert response.status == '200 OK'

def test_recipes(client):
    response = client.get('/recipes', follow_redirects=True)
    assert response.status == '200 OK'

def test_admin_links(client, auth):
    response = client.get('/')
    assert not b"Admin Log Out" in response.data
    assert not b"Admin Change Password" in response.data

    auth.login()
    response = client.get('/')
    assert b"Admin Log Out" in response.data
    assert b"Admin Change Password" in response.data

def test_admin_edit(client, auth):
    response = client.get('/projects')
    assert not b"Toggle" in response.data
    assert not b"Edit" in response.data

    auth.login()
    response = client.get('/projects')
    assert b"Toggle" in response.data
    assert b"Edit" in response.data

def test_toggle(client, auth):
    #not logged in user cannot toggle
    response = client.get('/project/toggle/1')
    assert b"Redirecting..." in response.data

    response = client.get('/projects')
    assert not b"Java" in response.data

    auth.login()
    response = client.get('/projects')
    assert b"Java" in response.data

    response = client.get('/project/toggle/500')
    assert response.status_code == 404

    client.get('/project/toggle/3')
    auth.logout()
    response = client.get('/projects')
    assert b"Java" in response.data


def test_delete(client, auth, app):
    #not logged in user cannot delete
    response = client.get('/project/delete/1')
    assert response.status_code == 405



    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM project').fetchone()[0]

    response = client.post('/project/delete/1')
    with app.app_context():
        db = get_db()
        secondcount = db.execute('SELECT COUNT(id) FROM project').fetchone()[0]
    assert count == secondcount

    auth.login()
    response = client.post('/project/delete/1')
    with app.app_context():
        db = get_db()
        thirdcount = db.execute('SELECT COUNT(id) FROM project').fetchone()[0]
    assert count == thirdcount + 1

def test_create(client, auth, app):
    auth.login()
    assert client.get('/project/create').status_code == 200

    client.post('/project/create', data={
                'shown' : 1, 
                'programming_language' : 'C#', 
                'tools_used' : 'Unity', 
                'title' : 'Random Game Dev', 
                'info' : 'Lorem Ipsum', 
                'link_github' : 'https://www.unity3d.com', 
                'link_live' : 'https://www.justinwcain.com', 
                'last_updated' : '2023-08-03' 
    })

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM project').fetchone()[0]
        assert count == 4

    response = client.post('/project/create', data={
                'shown' : 1, 
                'programming_language' : 'C#', 
                'tools_used' : 'Unity', 
                'title' : '', 
                'info' : 'Lorem Ipsum', 
                'link_github' : 'https://www.unity3d.com', 
                'link_live' : 'https://www.justinwcain.com', 
                'last_updated' : '2023-08-03' 
    })
    assert re.search('Title is required.', response.get_data(as_text=True)) 
    response = client.post('/project/create', data={
                'shown' : 1, 
                'programming_language' : 'C#', 
                'tools_used' : 'Unity', 
                'title' : 'title', 
                'info' : '', 
                'link_github' : 'https://www.unity3d.com', 
                'link_live' : 'https://www.justinwcain.com', 
                'last_updated' : '2023-08-03' 
    })
    assert re.search('Project Info is required.' , response.get_data(as_text=True))

def test_update(client, auth, app):
    auth.login()
    assert client.get('project/update/1').status_code == 200
    response = client.post('/project/update/1', data={
                'shown' : 1, 
                'programming_language' : 'C#', 
                'tools_used' : 'Unity', 
                'title' : 'title_updated', 
                'info' : '123123', 
                'link_github' : 'https://www.unity3d.com', 
                'link_live' : 'https://www.justinwcain.com', 
                'last_updated' : '2023-08-03' 
    })
    with app.app_context():
        db = get_db()
        project = db.execute('SELECT * FROM project WHERE id = 1').fetchone()
        assert project['title'] == 'title_updated'

    response = client.post('/project/update/1', data={
                'shown' : 1, 
                'programming_language' : 'C#', 
                'tools_used' : 'Unity', 
                'title' : '', 
                'info' : 'Lorem Ipsum', 
                'link_github' : 'https://www.unity3d.com', 
                'link_live' : 'https://www.justinwcain.com', 
                'last_updated' : '2023-08-03' 
    })
    assert re.search('Title is required.', response.get_data(as_text=True)) 
    response = client.post('/project/update/1', data={
                'shown' : 1, 
                'programming_language' : 'C#', 
                'tools_used' : 'Unity', 
                'title' : 'title', 
                'info' : '', 
                'link_github' : 'https://www.unity3d.com', 
                'link_live' : 'https://www.justinwcain.com', 
                'last_updated' : '2023-08-03' 
    })
    assert re.search('Project Info is required.' , response.get_data(as_text=True))