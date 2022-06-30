from flask import Flask, render_template, redirect, request, make_response, abort
import jwt


with open('secret.txt', 'r') as f:
    secret_key = f.read()

with open('secret2.txt', 'r') as f:
    secret_key2 = f.read()


app = Flask(__name__)


@app.route('/')
def login():
    try:
        token = request.cookies.get('token')
        token = jwt.decode(token, secret_key, algorithms=['HS256'])
        if token['username'] != 'benthecat': raise Exception('Invalid token')
    except Exception:
        pass
    else:
        return redirect('/home')

    return render_template('login.html')


@app.route('/auth', methods=["post"])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'benthecat' and password == 'meoww':
        token = jwt.encode({'username': username, 'type': 'user'}, secret_key, algorithm='HS256')
        resp = make_response(redirect("/home"))
        resp.set_cookie('token', token)
        return resp
    return redirect('/')


@app.route('/home')
def home():
    try:
        token = request.cookies.get('token')
        token = jwt.decode(token, secret_key, algorithms=['HS256'])
        if token['username'] != 'benthecat': raise Exception('Invalid token')
    except Exception:
        return abort(403)

    return render_template('home.html')


@app.route('/admin')
def admin():
    try:
        token = request.cookies.get('token')
        token = jwt.decode(token, secret_key, algorithms=['HS256'])
        if token['username'] != 'benthecat' or token['type'] != 'admin': raise Exception('Invalid token')
    except Exception:
        return abort(403)

    return render_template('admin.html')


@app.route('/bonus')
def bonus():
    try:
        token = request.cookies.get('token')
        token = jwt.decode(token, secret_key2, algorithms=['none', 'HS256'])
        if token['username'] != 'benthecat' or token['type'] != 'bonus': raise Exception('Invalid token')
    except Exception:
        return abort(403)

    return render_template('bonus.html')


@app.route('/secret')
def secret():
    return secret_key


if __name__ == '__main__':
    app.run(debug=True)
