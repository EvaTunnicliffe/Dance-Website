from flask import Flask, render_template, request, redirect, url_for
from db_functions import run_search_query_tuples, run_commit_query
from datetime import datetime

app = Flask(__name__)
db_path = 'data/dance_db.sqlite'


@app.template_filter()
def newsdate(sqlite_dt):
    # create a data object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %y %I:%M %p")


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


@app.route('/notices')
def notices():
    # query for the page
    sql = """select news.news_id, news.title, news.subtitle, news.content, news.newsdate, member.name
    from news
    join member on news.member_id = member.member_id
    order by news.newsdate desc;
    """

    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("notices.html", news=result)


@app.route('/news_cud', methods=['GET', 'POST'])
def news_cud():
    # collect data from the web address
    data = request.args
    print(data)
    required_keys = ['id', 'task']
    for k in required_keys:
        if k not in data.keys():
            message = " Could not get the right keys for news CUD"
            return render_template("error.html", message=message)
    # have an id and a task key
    if request.method == 'GET':
        if data['task'] == 'delete':
            sql = "delete from news where news_id =?"
            values_tuple = (data['id'],)
            result= run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('notices'))

        elif data['task'] == 'update':
            sql = """ select title, subtitle, content from news where news_id=?"""
            values_tuple = (data['id'],)
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("news_cud.html",
                                   **result,
                                   id=data['id'],
                                   task=data['task'])


        elif data['task'] == 'add':
            # dummy data for testing
            temp = {'title' : 'Test Title' , 'subtitle' : 'Test Subtitle' , 'content' : 'Test Content'}
            return render_template("news_cud.html",
                                   id=0,
                                   task=data['task'],
                                   **temp)
        else:
            message = "Unrecognised task coming from news page"
            return render_template("error.html", message=message)
    elif request.method == 'POST':
        # collected form information
        f = request.form
        print(f)

        if data['task'] == 'add':
            # add the new news entry to the database
            # member is fixed for now
            sql = """insert into news(title, subtitle, content, newsdate, member_id)
                        values(?,?,?,datetime('now', 'localtime'),2)"""
            values_tuple = (f['title'], f['subtitle'], f['content'])
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('notices'))

        elif data['task'] == 'update':
            sql = """update news set title=?, subtitle=?, content=?, newsdate=datetime('now', 'localtime') where news_id=?"""
            values_tuple = (f['title'], f['subtitle'], f['content'], data['id'])
            result = run_commit_query(sql, values_tuple, db_path)
            # collect the data from the form and update the database at the sent id
            return redirect(url_for('notices'))

@app.route('/login', methods=["GET", "POST"])
def login():
    error = "Your credentials are not recognised"
    if request.method == "GET":
        return render_template("/login.html", email='vanny@yahoo.com', password='temp')
    elif request.method == "POST":
        f=request.form
        print(f)
        sql = """select name, password, authorisation from member where email = ?"""
        values_tuple=(f['email'],)
        result = run_search_query_tuples(sql, values_tuple, db_path, True)
        if result:
            result = result[0]
            if result['password'] == f['password']:
                print("Login okay")
                return redirect(url_for('index'))
            else:
                return render_template("/login.html", email='vanny@yahoo.com', password='temp', error=error)

        else:
            return render_template("/login.html", email='vanny@yahoo.com', password='temp', error=error)



if __name__ == "__main__":
    app.run(debug=True)