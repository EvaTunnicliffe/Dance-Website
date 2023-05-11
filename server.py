from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/classes')
def classes():
    return render_template("classes.html")


@app.route('/teachers')
def teachers():
    return render_template("teachers.html")


@app.route('/enrol', methods=["GET", "POST"])
def enrol():
    if request.method == "POST":
        f = request.form
        print(f)
        return render_template("confirm.html", form_data=f)
    elif request.method == "GET":
        temp_form_data = {
            "fullname": "Eva Tunnicliffe",
            "email": "eva.wgtn@gmail.com",
            "age": "17",
            "aboutme": "Hello",
            "problems": "No",
            "consent": "Yes",
            "how": "Through friends"
        }
        return render_template("enrol.html", **temp_form_data)


if __name__ == "__main__":
    app.run(debug=True)