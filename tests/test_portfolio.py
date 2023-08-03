from JustinWCainPortfolio import create_app

def test_resume(client):
    response = client.get('/resume', follow_redirects=True)
    assert response.status == '200 OK'

def test_projects(client):
    response = client.get('/projects', follow_redirects=True)
    assert response.status == '200 OK'

def test_recipes(client):
    response = client.get('/recipes', follow_redirects=True)
    assert response.status == '200 OK'