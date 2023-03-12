from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

class DBUsers:
    db = 'email.txt'  # json objects line by line

    @classmethod
    def is_email_exists(cls, email):
        with open(cls.db, 'r') as fd:
            while obj_line := fd.readline():
                user = json.loads(obj_line)
                if user.get('email') == email:
                    return True
        return False

    @classmethod
    def save_email(cls, email, password):
        with open(cls.db, 'a') as fd:
            if fd.tell() > 0:  # avoid first line separator
                data = '\n'
            else:
                data = ''

            data += json.dumps(obj={'email': email, 'password': password})
            fd.write(data)
        return True

    @classmethod
    def check_password(cls, email, password):
        with open(cls.db, 'r') as fd:
            while obj_line := fd.readline():
                user = json.loads(obj_line)
                if user.get('email') == email:
                    if user.get('password') == password:
                        return True
                    else:
                        return False
        return False



@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', 'none')
        return render_template('index.html', context={'name': name})
    else:

        return render_template('index.html', context={'name': 'Anon'})

@app.route("/registration", methods=['GET','POST'])
def registration():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', 'none')
        if DBUsers.is_email_exists(email=email):
            # email already exists
            return redirect(f'/login?email={email}')
        else:
            # email not exists
            DBUsers.save_email(email=email, password=password)
        return render_template('index.html', context={'name': email})
    else:  #  request.method == 'GET':
        return render_template('registration.html', context={'name': ''})

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', None)
        if DBUsers.check_password(email=email, password=password):
            return redirect(url_for('registration_finished', email=email))
        else:
            # check_password is failed
            return redirect(url_for('login', email=email, failed=True))

    context = {}
    if 'email' in request.args:
        context['email'] = request.args.get('email')
    if 'failed' in request.args:
        context['failed'] = True
    return render_template('login.html', context=context)


@app.route("/registration_finished")
def registration_finished():
    if 'email' in request.args:
        context = {'email': request.args.get('email'), 'login_success': True}
    return render_template('index.html', context=context)

