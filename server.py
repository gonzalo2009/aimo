# Run with "python server.py"
from bottle import run, get, post, hook, response, request, redirect
import jwt
from models import User, Note
from serializers import UserSchema, NoteSchema
from werkzeug.security import generate_password_hash, check_password_hash

# Start your code here, good luck (: ...
key = 'secret'


def is_logged_in(func):
    def wrapper():
        token = request.get_cookie("token")
        if token:
            return func()
        return {'message': 'Not logged in'}
    return wrapper


def get_user():
    token = request.get_cookie("token")
    user_data=jwt.decode(token.encode(), key, algorithm="HS256")
    username = user_data['username']
    user = User.get(username=username)
    return user


@post('/api/add_note')
@is_logged_in
def add_note():
    user = get_user()
    message = request.POST['message']
    note = Note(user=user, message=message)
    note.save()
    return {'note': note.message}


@get('/api/get_notes')
@is_logged_in
def get_notes():
    user = get_user()
    notes = [i['message'] for i in NoteSchema(many=True).dump(user.notes).data]
    if notes:
        return {'notes': notes}
    else:
        return {'notes': 'The list is empty.'}


@post('/api/register_user')
def register_user():
    username = request.POST['username']
    password = request.POST['password']
    if not User.select().where(User.username == username):
        user = User(username=username, password=generate_password_hash(password))
        user.save()
        user_data = UserSchema().dump(user).data
        token = jwt.encode(user_data, key, algorithm="HS256")
        response.set_cookie("token", token.decode())
        return {'username': user_data['username'], 'password': user_data['password']}
    else:
        return {'message': 'The username already exists.'}


@post('/api/login')
def login():
    username = request.POST['username']
    password = request.POST['password']
    if User.select().where(User.username == username):
        user = User.get(username=username)
        user_data = UserSchema().dump(user).data
        if check_password_hash(user.password, password):
            token = jwt.encode(user_data, key, algorithm="HS256").decode()
            response.set_cookie("token", token)
            return {'message': 'successfully logged in'}
    return {'message': 'Login failed.'}


@get('/api/logout')
@is_logged_in
def logout():
    response.delete_cookie('token')
    return {'message': 'successfully logged out'}



run(host='localhost', port=8000, reloader=True)

