# app.py : Windows 10 C:/flaskprod/bblog2428/app.py
import sqlite3
import os
from pathlib import Path
import platform
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from datetime import datetime, date, timedelta
from dateutil.parser import parser
from icecream import ic
import django_heroku
import dj_database_url
from decouple import config

# Define secret key to insure security
# NOTE: 'secret_key' was transferred to .env file upon
#       transition to Heroku.

# Determine the current OS and set the DB Path accordingly
def get_db_name():
    # Test for "Windows", "Linux", or "Macbookpro(Darwin)"
    # current_os = platform.system(); OS_Found = True;
    # home_path=os.getcwd()
    # Set a 'cross-platform' path to the DB file 
    db_path = Path('bibleblog.sqlite')
    if db_path.is_file():
        return db_path.name
    else:
        return "Unknown DB file"

# Establish connection to the sqlite3 DB
def get_db_connection():
    db_name = get_db_name()
    #ic('get_dbconnection(): ', db_name)
    con = sqlite3.connect(db_name)
    con.row_factory = sqlite3.Row
    return con

app = Flask(__name__)
# Following setting transferred to variable in .env file
# for Heroku deployment: 1/27/25
#app.config['SECRET_KEY'] = secret_key

# Set globals
Today = date.today()
iDate = date(2024,12,1)
Id = (Today - iDate).days + 1

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    #ic('date: ', date)
    y=int(date[0:4]);m=int(date[5:7]);d=int(date[8:10])
    #ic('Jinja2: ',type(y),type(m),type(d))
    date_=date(y,m,d)
    pdate = parser.parse(date_).strftime("%Y-%m-%d-%H-%M")
    native = date.replace(tzinfo=None)
    #ic('native: ', native)
    format='%a %Y-%m-%d'
    return native.strftime(format) 

def get_readings(r_id):
    conn = get_db_connection()
    reads = conn.execute("""SELECT Bid, Bdate, Book, Chapter, Feedback
                            FROM bblog2428
                            WHERE Bid=?""",(r_id,)).fetchone()
    return reads

def form_dt(Bdt):
    yr=int(Bdt[0:4]); mo=int(Bdt[5:7]); dy=int(Bdt[8:10])
    return date(yr,mo,dy).strftime("%a %Y-%m-%d")

# Define all routes for the APP
@app.route('/')
def index():
    global Id
    # Generate default record Id for today's readings
    reads = get_readings(Id)
    tdate = form_dt(reads['Bdate'])
    return render_template('index.html', reads=reads, tdate=tdate)

@app.route('/<int:Post_Id>/get/', methods=['GET', 'POST'])
def get(Post_Id):
    reads = get_reading(Post_Id)
    conn = get_db_connection()
    read = conn.execute("""SELECT * FROM bblog2428
                                    WHERE Bid=?""",(Post_Id,)).fetchone()
    conn.close()
    return render_template('get.html', read=read)

# Edit blog post
@app.route('/<int:Id>/edit/', methods=('GET', 'POST'))
def edit(Id):
    reads = get_readings(Id)
    if request.method == 'POST':
        bid = reads['Bid']
        bdate = form_dt(reads['Bdate'])
        fb = request.form.get('feedback')
        # Verify user input field
        goback = False
        if not bid:
            flash('Bid is required!'); goback = True
        if not fb:
            flash('Feedback is required!'); goback = True
        if goback:
            flash('Record update failed.')
            return redirect(url_for('index'))
        else:
            conn = get_db_connection()
            conn.execute("""UPDATE bblog2428
                            SET Feedback=?
                            WHERE Bid=?""",(fb, bid))
            message = "%d has been updated." % (bid)
            flash(message)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('edit.html', reads=reads)

@app.route('/<int:yrm>/report')
def report(yrm):
    yym=str(yrm)
    # Generate string values for date values for SQL query
    yr=str(f"{'20'+ yym[0:2]}"); mn=str(f"{yym[2:]}").zfill(2)
    req_date = date(int(yr), int(mn), 1)
    Month=req_date.strftime('%B %Y')
    con = get_db_connection()
    sql_ = """SELECT * FROM bblog2428 WHERE substr(Bdate,1,4)=?
                        AND substr(Bdate,6,2)=?"""
    reads = con.execute(sql_,(yr,mn)).fetchall()
    return render_template('report.html', reads=reads, Month=Month)

# Generate books list for those without feedback
@app.route('/books')
def books():         # Parm = book name from the DB
    #Bk = bk.capitalize();
    #Book_name = books_dict.get(Bk)
    Title="Count of Chapters with Feedback"
    con = get_db_connection()
    reads = con.execute("""SELECT Book, min(Bid), count(Chapter), count(Feedback)
                                    FROM bblog2428
                                    GROUP BY Book
                                    HAVING count(Feedback)<>'None'
                                    ORDER BY min(Bid)""").fetchall()
    #for read in reads:
    #    print(reads[0],read[1],read[2])
    return render_template('books.html', reads=reads, Title=Title)



if __name__=="__main__":
    app.run(debug=True)
#
