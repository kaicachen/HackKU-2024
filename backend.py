from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
from datetime import date

app = Flask(__name__)
app.secret_key = "hello"
today = date.today()

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

@app.route("/create_account")
def create_account():
    return render_template("createaccount.html")
    

@app.route("/account_success", methods = ["POST"])
def account_success():
    username = request.form.get("username")
    password = request.form.get("password")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    location = request.form.get("location")

    session["username"] = username
    session["password"] = password
    session["firstname"] = firstname
    session["lastname"] = lastname
    session["location"] = location

    cursor = mysql.connection.cursor()

    

    query= "INSERT INTO users (username, passwd, firstname, lastname, location) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query,(username,password,firstname,lastname,location,))
    mysql.connection.commit()
    
    cursor.close()

    return render_template("account_success.html")


@app.route("/login", methods = ["GET","POST"])
def login():
    if session.get("username") is None:
        return render_template("login.html")
        
    else:
        return render_template("login_success.html")

@app.route("/login_info", methods = ["GET","POST"])
def login_info():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        cursor = mysql.connection.cursor()

        query= "SELECT * FROM users WHERE username = %s"
        cursor.execute(query,(username,))
        result = cursor.fetchone()
        
        if result is not None:
            session["username"] = username
            session["password"] = password
            return render_template("login_success.html")
        
        else:    
            return redirect(url_for("create_account"))   

    

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("index"))

@app.route("/process_form", methods = ["POST"])
def process():
    if request.method == "POST":
        username = session["username"]
        date = request.form.get("date")
        results = []
        cursor = mysql.connection.cursor()
        query1 = "SELECT score FROM logs WHERE username = %s AND date = %s"
        query2 = "SELECT note FROM logs WHERE username = %s AND date = %s"
        cursor.execute(query1,(username,date,))
        result1 = cursor.fetchone()
        cursor.execute(query2,(username,date,))
        result2 = cursor.fetchone()

        results.append(result1)
        results.append(result2)
        cursor.close()
        

        if date == str(today):
            if result1 is None or result2 is None:
                return render_template("track.html")
            else:
                output = " | ".join(str(element) for sublist in results for element in sublist)
                string_date = str(date)
                return f'<p>{string_date}: {output}</p>'
        else:
            if result1 is None or result2 is None:
                return render_template("no_result.html")
            else:   
                output = " | ".join(str(element) for sublist in results for element in sublist)
                string_date = str(date)
                return f'<p>{string_date}: {output}</p>'




@app.route("/mood")
def mood():
    return render_template("mood.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/calendar")
def calendar():
    if session.get("username") is None:
        return redirect(url_for("login"))
        
    else:
        return render_template("calendar.html")

@app.route("/track", methods=["POST"])
def track():
    if request.method == "POST":
        username = session["username"]
        score = int(request.form.get("mood_score"))
        note = request.form.get("note")
        date = str(today)
        results = []
        cursor = mysql.connection.cursor()
        query1 = "INSERT INTO logs (username, date, score, note) VALUES (%s, %s, %s, %s)"
        cursor.execute(query1, (username, date, score, note,))
        mysql.connection.commit()  # Commit changes to the database
        query2 = "SELECT score FROM logs WHERE username = %s AND date = %s"
        cursor.execute(query2, (username, date,))
        result = cursor.fetchone()
        cursor.close()
        results.append(result)
        output = " | ".join(str(element) for sublist in results for element in sublist)
        string_date = str(date)
        return f'<p>{string_date}: {output}</p>'
    


if __name__ == '__main__':
    app.run()