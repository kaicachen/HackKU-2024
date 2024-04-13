from flask import Flask, render_template, request
from flask_mysqldb import MySQL


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'TN9VVQ%YPHu45YLftak$'
app.config['MYSQL_DB'] = 'mental_health'


@app.route("/")
def hello_world():
    return render_template('frontpage.html')

@app.route("/process_form")
def process():
    if request.method == "POST":
        name = request.form.get()


@app.route("/mood")
def mood():
    return render_template('mood.html')
    


if __name__ == '__main__':
    app.run()