from JustinWCainPortfolio import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_resume(client):
    response = client.get('/resume', follow_redirects=True)
    assert response.status == '200 OK'