from app import create_app
from extensions import db
from sqlalchemy import text

app = create_app()
app.testing = True

with app.app_context():
    conn = db.session.connection()
    tables = [
        'user',
        'posts',
        'comments',
        'profile',
        'likes',
        'reported_content',
    ]
    for table in tables:
        try:
            print(f'--- TABLE {table} ---')
            for row in conn.execute(text(f'SHOW COLUMNS FROM `{table}`')):
                print(row)
        except Exception as exc:
            print(f'ERROR inspecting {table}:', type(exc).__name__, exc)

client = app.test_client()
username = 'user_' + ''.join(__import__('random').choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6))
email = username + '@example.com'
password = 'Password1!'
print('REGISTER', username, email)
r = client.post('/auth/register', data={
    'username': username,
    'email': email,
    'password': password,
    'confirm_password': password,
})
print('register status', r.status_code)
print(r.location)
print(r.data.decode('utf-8', errors='ignore')[:500])

print('LOGIN')
r = client.post('/auth/login', data={'email': email, 'password': password})
print('login status', r.status_code)
print(r.location)
print(r.data.decode('utf-8', errors='ignore')[:500])

print('FEED')
r = client.get('/feed')
print('feed status', r.status_code)
print('feed length', len(r.data))

print('POST CREATE')
r = client.post('/posts/create', data={'content': 'Test content'}, follow_redirects=True)
print('post create status', r.status_code)
print('post create final path', r.request.path)
print(r.data.decode('utf-8', errors='ignore')[:500])

print('PROFILE VIEW')
r = client.get(f'/profile/{1}')
print('profile status', r.status_code)
print(r.request.path)
print(r.data.decode('utf-8', errors='ignore')[:500])
