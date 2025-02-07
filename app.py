# app.py : Windows 10 /c/Users/Ed/Desktop/flaskprod/bblog2428/app.py
#        : Installed gunicorn on 2/7/25
#        : Updated bblog2428 on Github on 2/7/25
#
import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from icecream import ic

# Set the environmental variables for APP
load_dotenv()                       # Load environment variables from .env file

db_name = os.getenv('DATABASE_URL')
db_url = 'sqlite:///' + db_name
secret_key = os.getenv('SECRET_KEY')

# Instantiate the Bibleblog APP
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

# Establish connection to the sqlite3 DB
def get_db_connection():
    global db_name
    con = sqlite3.connect(db_name)
    con.row_factory = sqlite3.Row
    return con

# Set globals
Today = date.today()
iDate = date(2024,12,1)
Id = (Today - iDate).days + 1

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
    yr = str(f"{'20'+ yym[0:2]}"); mo = str(f"{yym[2:]}").zfill(2)
    req_date = date(int(yr), int(mo), 1)
    Month=req_date.strftime('%B %Y')
    conn = get_db_connection()
    sql_ = """SELECT * FROM bblog2428 WHERE substr(Bdate,1,4)=?
                        AND substr(Bdate,6,2)=?"""
    reads = conn.execute(sql_,(yr,mo)).fetchall()
    conn.close()
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
    app.run()
#
