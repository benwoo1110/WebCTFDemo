from flask import Flask, render_template, send_file, redirect, request, make_response, abort
import jwt


with open('secret.txt', 'r') as f:
    secret_key = f.read()


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
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
    return redirect('/login')


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
        token = jwt.decode(token, secret, algorithms=['HS256'])
        if token['username'] != 'benthecat' or token['type'] != 'admin': raise Exception('Invalid token')
    except Exception:
        return abort(403)

    return render_template('admin.html')


@app.route('/robots.txt')
def robots():
    return send_file("robots.txt")


@app.route('/secret')
def secret():
    return secret


if __name__ == '__main__':
    app.run(debug=True)
