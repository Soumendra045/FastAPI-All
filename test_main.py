from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_all_get_blog():
    responses = client.get('/blog/all')
    assert responses.status_code == 200

def test_auth_error():
    response = client.post('/token',
    data={'username':"",'password':""}                       
    )
    access_token = response.json().get('access-token')
    assert access_token == None
    # message = response.json().get("detail")[0].get("msg")
    # assert message == "Field required"

def test_auth_sucess():
    response = client.post('/token',
    data={'username':"cat",'password':"cat"}                       
    )
    assert response.status_code == 200
    data = response.json()
    access_token = data.get('access_token')
    assert access_token 


def test_post_article():
    auth = client.post('/token',
    data={'username':"cat",'password':"cat"}                       
    )
    data = auth.json()
    access_token = data.get('access_token')

    assert access_token

    response = client.post(
        '/article',
        json={
            'title':'test article',
            'content': 'tset coontent',
            'published': True,
            'creator_id':3
        },
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )

    assert response.status_code==200

    assert response.json().get('title') == 'test article'