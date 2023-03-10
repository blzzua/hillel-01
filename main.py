from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', 'none')
        return render_template('index.html', context={'name': name})
    else:

        return render_template('index.html', context={'name': 'Anon'})

@app.route("/new")
def new():
    print(request.args)
    pass
    return "200"
