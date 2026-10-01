def test_home(client):
 r=client.get('/')
 assert r.status_code==200
 assert 'FitBuddy' in r.text

def test_health(client):
 assert client.get('/api/health').json()['status']=='healthy'
