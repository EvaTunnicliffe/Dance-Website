from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return"<h1>Hello World</h1>"

@app.route('/classes')
def classes():
    return"<h1>Classes Page</h1>"

@app.route('/teachers')
def teachers():
    return"<h1>Teachers Page</h1>"

@app.route('/enrol')
def enrol(id):
    return"<h1>Enrol Page</h1> "


if __name__ == "__main__":
    app.run(debug=True)