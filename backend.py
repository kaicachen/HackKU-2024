from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder="templates", static_folder="static")


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'TN9VVQ%YPHu45YLftak$'
app.config['MYSQL_DB'] = 'mental_health'

mysql = MySQL(app)




@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/index", methods = ["GET", "POST"])
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

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

@app.route('/add_mood/<int:day>', methods=['GET', 'POST'])
def add_mood(day):
    if request.method == 'POST':
        # Get mood data from the form and insert into the database
        mood = request.form['mood']
        # Insert mood data into MySQL database
        # Your MySQL insertion code here...

        # You can return a JSON response or simply a success message if needed
        return {'success': True}

    return render_template('add_mood_popup.html', day=day)


@app.route("/mood")
def mood():
    return render_template('mood.html')

@app.route("/calendar")
def calendar():
    return render_template('calendar.html')

@app.route("/about")
def about():
    return render_template('about.html')
    


if __name__ == '__main__':
    app.run()