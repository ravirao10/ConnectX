import random
import string
import traceback
from app import create_app

app = create_app()
app.testing = True
app.config['PROPAGATE_EXCEPTIONS'] = True
client = app.test_client()

username = 'user_' + ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6))
email = username + '@example.com'
password = 'Password1!'
print('Registering', username, email)
try:
    r = client.post('/auth/register', data={
        'username': username,
        'email': email,
        'password': password,
        'confirm_password': password,
    }, follow_redirects=True)
    print('register', r.status_code)
except Exception:
    print('register exception')
    traceback.print_exc()

try:
    r = client.post('/auth/login', data={'email': email, 'password': password}, follow_redirects=True)
    print('login', r.status_code)
except Exception:
    print('login exception')
    traceback.print_exc()

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
    ('GET', '/admin/posts'),
    ('GET', '/admin/comments'),
    ('GET', '/admin/reports'),
]

for method, path, *rest in routes:
    data = rest[0] if rest else None
    print('---', method, path)
    try:
        if method == 'GET':
            resp = client.get(path, follow_redirects=True)
        else:
            resp = client.post(path, data=data or {}, follow_redirects=True)
        print('status', resp.status_code)
        if resp.status_code >= 500:
            print(resp.data.decode('utf-8', errors='ignore')[:1000])
    except Exception:
        print('exception for', path)
        traceback.print_exc()
