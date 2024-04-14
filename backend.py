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
app.config['MYSQL_PASSWORD'] = 'mmmHungwy?'
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
        

        if date == today:
            if result1 is None or result2 is None:
                return redirect(url_for("track.html"))
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

@app.route('/add_mood/<int:day>', methods=['GET', 'POST'])
def add_mood(day):
    if request.method == 'POST':
        # Get mood data from the form and insert into the database
        username = request.form.get["username"]

        # Insert mood data into MySQL database
        # Your MySQL insertion code here...

        # You can return a JSON response or simply a success message if needed
        return {'success': True}

    return render_template('add_mood_popup.html', day=day)


@app.route("/mood")
def mood():
    return render_template("mood.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")
    
@app.route('/plot')
def plot():
    # Fetch data from MySQL
    cursor = mysql.connection.cursor()
    username = session["username"]
    cursor.execute("SELECT date, score FROM logs WHERE username = %s", (username,))
    rows = cursor.fetchall()
    cursor.close()

    # Extract dates and scores
    dates = [row[0] for row in rows]
    scores = [row[1] for row in rows]

    # Convert dates to string format
    dates_str = [str(date) for date in dates]

    # Generate a list of days in the month
    days_in_month = 30  # Assuming a month with 30 days
    list_of_days = np.arange(1, days_in_month + 1)

    # Initialize an array to hold scores for each day
    scores_by_day = np.full(days_in_month, np.nan)

    # Populate the array with scores
    for date, score in zip(dates, scores):
        day = date.day
        scores_by_day[day - 1] = score

    # Interpolate missing scores
    nan_indices = np.isnan(scores_by_day)
    not_nan_indices = ~nan_indices
    interpolated_scores = np.interp(np.arange(days_in_month), np.arange(days_in_month)[not_nan_indices], scores_by_day[not_nan_indices])

    # Plot the graph
    plt.figure(figsize=(10, 5))
    
    plt.plot(list_of_days[not_nan_indices], scores_by_day[not_nan_indices], marker='o', color='blue', label='Entered day')
    plt.plot(list_of_days[nan_indices], interpolated_scores[nan_indices], marker='o', linestyle='None', color='red', label='Not entered')
    plt.title('Scores Over Days of the Month')
    plt.xlabel('Day')
    plt.ylabel('Mood (out of 10)')
    plt.xticks(list_of_days)
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