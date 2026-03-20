def test_put_user(api_client):
    payload = {
        'name': 'morpheus',
        'job': 'leader'
    }

    response = api_client.put('/users/2', json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body['name'] == 'morpheus'
    assert body['job'] == 'leader'

def test_patch_user(api_client):
    payload = {
        'job': 'AQA engineer'
    }

    response = api_client.patch('/users/2', json=payload)
    assert response.status_code == 200
    assert response.json()['job'] == 'AQA engineer'

def test_delete_user(api_client):
    response = api_client.delete('/users/2')

    assert response.status_code == 204

def test_get_users_with_params(api_client):
    response = api_client.get('/users', params={'page': 2})

    assert response.status_code == 200
    assert response.json()['page'] == 2