from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'TN9VVQ%YPHu45YLftak$'
app.config['MYSQL_DB'] = 'mental_health'

mysql = MySQL(app)




@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/process_form", methods = ["POST"])
def process():
    if request.method == "POST":
        username = request.form.get("username")
        date = request.form.get("date")

        cursor = mysql.connection.cursor()
        query = "SELECT note FROM logs WHERE username = %s AND date = %s"

        cursor.execute(query,(username,date,))
        result = cursor.fetchall()
        cursor.close()

        return str(result[0][0])


@app.route("/mood")
def mood():
    return render_template('mood.html')
    


if __name__ == '__main__':
    app.run()