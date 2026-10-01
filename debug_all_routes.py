import random
import string
import re
from app import create_app
from extensions import db
from models.post import Post
from models.user import User

app = create_app()
app.testing = True
client = app.test_client()

# Register and log in a user for auth-required endpoints.
username = 'user_' + ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6))
email = username + '@example.com'
password = 'Password1!'
print('register user', username, email)
register_resp = client.post('/auth/register', data={
    'username': username,
    'email': email,
    'password': password,
    'confirm_password': password,
}, follow_redirects=True)
print('register status', register_resp.status_code)
login_resp = client.post('/auth/login', data={'email': email, 'password': password}, follow_redirects=True)
print('login status', login_resp.status_code)

with app.app_context():
    user = User.query.filter_by(email=email).first()
    if not user:
        raise RuntimeError('User not found after register')
    user_id = user.id
    post = Post(user_id=user_id, content='Debug post content')
    db.session.add(post)
    db.session.commit()
    post_id = post.id
    print('created post', post_id)
    comment_id = None

sample_values = {
    'user_id': str(user_id),
    'post_id': str(post_id),
    'comment_id': '1',
    'admin_id': str(user_id),
}

routes = []
for rule in app.url_map.iter_rules():
    if rule.endpoint.startswith('static'):
        continue
    if rule.rule.startswith('/_'):
        continue
    path = rule.rule
    path = re.sub(r'<int:([^>]+)>', lambda m: sample_values.get(m.group(1), '1'), path)
    path = re.sub(r'<[^>]+>', '1', path)
    methods = sorted(method for method in rule.methods if method not in ('HEAD', 'OPTIONS'))
    routes.append((path, methods, rule.endpoint))

print('testing routes', len(routes))

payload_map = {
    '/auth/register': {'username': username + '2', 'email': 'other_' + email, 'password': password, 'confirm_password': password},
    '/auth/login': {'email': email, 'password': password},
    '/posts/create': {'content': 'Debug route content'},
    '/comments/add/1': {'content': 'Nice comment'},
    '/report/post/1': {'reason': 'Spam'},
    '/admin/delete/post/1': {},
    '/admin/delete/comment/1': {},
    '/admin/block/user/1': {},
    '/admin/unblock/user/1': {},
}

for path, methods, endpoint in routes:
    for method in methods:
        if method == 'GET':
            try:
                resp = client.get(path, follow_redirects=True)
            except Exception as exc:
                print('ERROR', method, path, endpoint, type(exc).__name__, exc)
                continue
        else:
            data = payload_map.get(path, {})
            try:
                resp = client.post(path, data=data, follow_redirects=True)
            except Exception as exc:
                print('ERROR', method, path, endpoint, type(exc).__name__, exc)
                continue
        if resp.status_code >= 500:
            print('FAIL', method, path, endpoint, resp.status_code)
            print(resp.data.decode('utf-8', errors='ignore')[:1000])
        elif resp.status_code >= 400:
            print('CLIENT ERROR', method, path, endpoint, resp.status_code)
        else:
            print('OK', method, path, endpoint, resp.status_code)
