import random
import string
from app import create_app
from extensions import db
from models.post import Post
from models.user import User

app = create_app()
app.testing = True
client = app.test_client()

username = 'user_' + ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6))
email = username + '@example.com'
password = 'Password1!'
print('Register')
r = client.post('/auth/register', data={
    'username': username,
    'email': email,
    'password': password,
    'confirm_password': password,
}, follow_redirects=True)
print('register', r.status_code)
print('login')
r = client.post('/auth/login', data={'email': email, 'password': password}, follow_redirects=True)
print('login', r.status_code)

with app.app_context():
    user = User.query.filter_by(email=email).first()
    print('user', user.id if user else None)
    post = Post(user_id=user.id, content='Test post for actions')
    db.session.add(post)
    db.session.commit()
    post_id = post.id
    print('created post', post_id)

print('like')
r = client.post(f'/like/{post_id}', follow_redirects=True)
print('like', r.status_code)
print(r.data.decode('utf-8', errors='ignore')[:300])

print('unlike')
r = client.post(f'/unlike/{post_id}', follow_redirects=True)
print('unlike', r.status_code)
print(r.data.decode('utf-8', errors='ignore')[:300])

print('comment add')
r = client.post(f'/comments/add/{post_id}', data={'content': 'Nice!'}, follow_redirects=True)
print('comment add', r.status_code)
print(r.data.decode('utf-8', errors='ignore')[:300])

print('report')
r = client.post(f'/report/post/{post_id}', data={'reason': 'Spam'}, follow_redirects=True)
print('report', r.status_code)
print(r.data.decode('utf-8', errors='ignore')[:300])
