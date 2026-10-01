from app import create_app
import random, string

app = create_app()
app.testing = True
client = app.test_client()

username = 'user_' + ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6))
email = username + '@example.com'
password = 'Password1!'
print('Registering', username, email)
r = client.post('/auth/register', data={
    'username': username,
    'email': email,
    'password': password,
    'confirm_password': password,
})
print('register', r.status_code, 'loc', r.location)

r = client.post('/auth/login', data={'email': email, 'password': password})
print('login', r.status_code, 'loc', r.location)

routes = [
    ('GET', '/'),
    ('GET', '/feed'),
    ('GET', '/users'),
    ('GET', f'/profile/1'),
    ('GET', f'/profile/1/edit'),
    ('GET', '/posts/create'),
    ('POST', '/posts/create', {'content': 'Debug route test'}),
    ('GET', '/admin'),
    ('GET', '/admin/dashboard'),
    ('GET', '/admin/users'),
]

for route in routes:
    method = route[0]
    path = route[1]
    data = route[2] if len(route) > 2 else None
    print('---', method, path)
    if method == 'GET':
        resp = client.get(path, follow_redirects=True)
    else:
        resp = client.post(path, data=data or {}, follow_redirects=True)
    request_path = resp.request.path if hasattr(resp, 'request') else 'N/A'
    print('status', resp.status_code, 'path', request_path)
    if resp.status_code == 500:
        print(resp.data.decode('utf-8', errors='ignore')[:1000])
    else:
        print('length', len(resp.data))
