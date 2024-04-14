from flask import Flask, render_template, request, session, redirect, url_for, send_file
from flask_mysqldb import MySQL
from datetime import date

import numpy as np
import matplotlib.pyplot as plt
import io
import mysql.connector

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
    
@app.route('/plot')
def plot():
	# Fetch data from MySQL
    cursor = mysql.connection.cursor()
    
    username = session["username"]
    cursor.execute("SELECT date, score FROM logs where username = %s")
    rows = cursor.fetchall()
    cursor.close()

	# Extract x and y values from the fetched data
    dates = [row[0] for row in rows]
    scores = [row[1] for row in rows]


    nan_indices = np.isnan(scores)
    not_nan_indices = ~nan_indices

    interpolated_scores = np.interp(np.flatnonzero(nan_indices), np.flatnonzero(not_nan_indices), scores[not_nan_indices])


    scores[nan_indices]

    coefficients = np.polyfit(np.arange(len(dates))[not_nan_indices], scores[not_nan_indices], 1)
    trendline = np.polyval(coefficients, np.arange(len(dates)))


    # Plot the graph
    plt.figure(figsize=(10, 5))
    plt.plot(dates[not_nan_indices], scores[not_nan_indices], marker='o', color='blue', label='Actual Scores')
    plt.plot(dates[nan_indices], interpolated_scores, marker='o', linestyle='None', color='red', label='Interpolated Scores')
    plt.plot(dates, trendline, linestyle='--', color='green', label='Trendline')
    plt.title('Scores Over Days of January 2022')
    plt.xlabel('Date')
    plt.ylabel('Mood score (out of 10)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()



    # Save plot to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
	# Clear plot
    plt.clf()
	# Return the image as a response
    return send_file(buffer, mimetype='image/png')



if __name__ == '__main__':
    app.run()