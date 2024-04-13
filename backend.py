from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "hello"

app.config['SESSION_COOKIE_NAME'] = 'session'  # Name of the session cookie
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Limit cookie access to HTTP requests
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookie over HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # SameSite policy for cookies




app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'TN9VVQ%YPHu45YLftak$'
app.config['MYSQL_DB'] = 'mental_health'

mysql = MySQL(app)



@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login", methods = ["GET","POST"])
def login():
    if session.get("username") is None:
        return render_template("login.html")
        
    else:
        return render_template("login_success.html")

@app.route("/login_info", methods = ["GET","POST"])
def login_info():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["username"] = username
        session["password"] = password
        return redirect(url_for("login"))   

    return render_template("login_success.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("index"))
    


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
    return render_template("mood.html")

@app.route("/mood_track")
def mood_track():
    return render_template("track.html")


@app.route("/process_track", methods = ["POST"])
def track():
    if request.method == "POST":
        date = request.form.get("date")
        mood = request.form.get("mood")
        note = request.form.get("note")
        username = session["username"]

        cursor = mysql.connection.cursor()
        query = ""

        cursor.execute(query,(username,date,))
        result = cursor.fetchall()
        cursor.close()

        return str(result[0][0])

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/calendar")
def calendar():
    if session.get("username") is None:
        return render_template("login.html")
    else:
        return render_template("calendar.html")
    
@app.route("/resources")
def resources():
    return render_template("resources.html")

if __name__ == '__main__':
    app.run()