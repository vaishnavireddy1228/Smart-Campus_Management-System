from flask import Flask,render_template,request,redirect
import sqlite3

app=Flask(__name__)

def connect():
    return sqlite3.connect("campus.db")

def create_tables():

    con=connect()
    cur=con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    branch TEXT,
    semester INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance(

id INTEGER PRIMARY KEY AUTOINCREMENT,

student TEXT,

subject TEXT,

present INTEGER,

total INTEGER

)
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS marks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student TEXT,
    subject TEXT,
    mark INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS fees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student TEXT,
    tuition INTEGER,
    hostel INTEGER,
    transport INTEGER,
    total INTEGER,
    paid INTEGER,
    remaining INTEGER,
    status TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eventname TEXT,
    participants TEXT
    )
    """)

    con.commit()
    con.close()
create_tables()


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/students",methods=["GET","POST"])
def students():

    con=connect()
    cur=con.cursor()

    if request.method=="POST":

        cur.execute(
        '''
        INSERT INTO students(
        name,age,branch,semester)
        VALUES(?,?,?,?)
        ''',
        (
        request.form["name"],
        request.form["age"],
        request.form["branch"],
        request.form["semester"]
        ))

        con.commit()

    cur.execute(
    "SELECT * FROM students"
    )

    data=cur.fetchall()

    con.close()

    return render_template(
    "students.html",
    students=data
    )


@app.route("/delete_student/<id>")
def delete_student(id):

    con=connect()
    cur=con.cursor()

    cur.execute(
    "DELETE FROM students WHERE id=?",
    (id,)
    )

    cur.execute(
    "SELECT COUNT(*) FROM students"
    )

    count=cur.fetchone()[0]

    if count==0:

        cur.execute(
        "DELETE FROM sqlite_sequence WHERE name='students'"
        )

    con.commit()

    con.close()

    return redirect("/students")




@app.route("/minus/<id>")
def minus(id):

 con=connect()

 cur=con.cursor()

 cur.execute(
 '''
 UPDATE attendance
 SET total=total-1
 WHERE id=?
 ''',
 (id,)
 )

 con.commit()

 con.close()

 return redirect("/attendance")



@app.route("/attendance",methods=["GET","POST"])
def attendance():

    con=connect()
    cur=con.cursor()

    if request.method=="POST":

        student=request.form["student"]
        subject=request.form["subject"]
        present=int(request.form["present"])
        total=int(request.form["total"])

        cur.execute(
'''
INSERT INTO attendance(
student,
subject,
present,
total)
VALUES(?,?,?,?)
''',
(
student,
subject,
present,
total
))

        con.commit()

    cur.execute(
    "SELECT * FROM attendance"
    )

    records=cur.fetchall()

    cur.execute(
    "SELECT name FROM students"
    )

    students=cur.fetchall()

    con.close()

    return render_template(
    "attendance.html",
    records=records,
    students=students
    )

@app.route("/plus_present/<id>")
def plus_present(id):

    con=connect()
    cur=con.cursor()

    cur.execute(
    "UPDATE attendance SET present=present+1 WHERE id=?",
    (id,)
    )

    con.commit()
    con.close()

    return redirect("/attendance")


@app.route("/minus_present/<id>")
def minus_present(id):

    con=connect()
    cur=con.cursor()

    cur.execute(
    '''
    UPDATE attendance
    SET present=
    CASE
    WHEN present>0
    THEN present-1
    ELSE 0
    END
    WHERE id=?
    ''',
    (id,)
    )

    con.commit()
    con.close()

    return redirect("/attendance")


@app.route("/plus_total/<id>")
def plus_total(id):

    con=connect()
    cur=con.cursor()

    cur.execute(
    "UPDATE attendance SET total=total+1 WHERE id=?",
    (id,)
    )

    con.commit()
    con.close()

    return redirect("/attendance")


@app.route("/minus_total/<id>")
def minus_total(id):

    con=connect()
    cur=con.cursor()

    cur.execute(
    '''
    UPDATE attendance
    SET total=
    CASE
    WHEN total>0
    THEN total-1
    ELSE 0
    END
    WHERE id=?
    ''',
    (id,)
    )

    con.commit()
    con.close()

    return redirect("/attendance")


@app.route("/delete_attendance/<id>")
def delete_attendance(id):

    con=connect()
    cur=con.cursor()

    cur.execute(
    "DELETE FROM attendance WHERE id=?",
    (id,)
    )

    con.commit()
    con.close()

    return redirect("/attendance")





@app.route("/marks",methods=["GET","POST"])
def marks():

    con=connect()
    cur=con.cursor()

    if request.method=="POST":

        student=request.form["student"]
        subject=request.form["subject"]
        mark=int(request.form["mark"])

        cur.execute(
        '''
        INSERT INTO marks(
        student,
        subject,
        mark
        )
        VALUES(?,?,?)
        ''',
        (
        student,
        subject,
        mark
        ))

        con.commit()

    cur.execute(
    "SELECT * FROM marks"
    )

    records=cur.fetchall()

    cur.execute(
    '''
    SELECT
    student,
    AVG(mark)

    FROM marks

    GROUP BY student
    '''
    )

    avgdata=cur.fetchall()

    grades=[]

    for s,avg in avgdata:

        if avg>=90:

            g="A"

        elif avg>=75:

            g="B"

        elif avg>=60:

            g="C"

        else:

            g="F"

        grades.append(
        (
        s,
        round(avg,2),
        g
        ))

    cur.execute(
    "SELECT name FROM students"
    )

    students=cur.fetchall()

    con.close()

    return render_template(
    "marks.html",
    records=records,
    grades=grades,
    students=students
    )


@app.route("/delete_mark/<id>")
def delete_mark(id):

    con=connect()
    cur=con.cursor()

    cur.execute(
    "DELETE FROM marks WHERE id=?",
    (id,)
    )

    con.commit()

    con.close()

    return redirect("/marks")

@app.route("/fees",methods=["GET","POST"])
def fees():

    con=connect()
    cur=con.cursor()

    if request.method=="POST":

        student=request.form["student"]

        tuition=int(
        request.form["tuition"])

        hostel=int(
        request.form["hostel"])

        transport=int(
        request.form["transport"])

        paid=int(
        request.form["paid"])

        total=(
        tuition+
        hostel+
        transport)

        remaining=(
        total-paid)

        if remaining<=0:

            status="Paid"

        else:

            status="Pending"

        cur.execute(
        '''
        INSERT INTO fees(
        student,
        tuition,
        hostel,
        transport,
        total,
        paid,
        remaining,
        status
        )
        VALUES(?,?,?,?,?,?,?,?)
        ''',
        (
        student,
        tuition,
        hostel,
        transport,
        total,
        paid,
        remaining,
        status
        ))

        con.commit()

    cur.execute(
    "SELECT * FROM fees"
    )

    data=cur.fetchall()

    cur.execute(
    "SELECT name FROM students"
    )

    students=cur.fetchall()

    con.close()

    return render_template(
    "fees.html",
    records=data,
    students=students
    )


@app.route("/delete_fee/<id>")
def delete_fee(id):

    con=connect()
    cur=con.cursor()

    cur.execute(
    "DELETE FROM fees WHERE id=?",
    (id,)
    )

    con.commit()

    con.close()

    return redirect("/fees")


@app.route("/edit_fee/<id>",
methods=["POST"])
def edit_fee(id):

    con=connect()
    cur=con.cursor()

    new_paid=int(
    request.form["paid"]
    )

    cur.execute(
    '''
    SELECT
    tuition,
    hostel,
    transport,
    paid

    FROM fees

    WHERE id=?
    ''',
    (id,)
    )

    old=cur.fetchone()

    total=(
    old[0]+
    old[1]+
    old[2]
    )

    current_paid=old[3]

    paid=(
    current_paid+
    new_paid
    )

    if paid>total:

        paid=total

    remaining=(
    total-paid
    )

    if remaining<=0:

        status="Paid"

    else:

        status="Pending"

    cur.execute(
    '''
    UPDATE fees

    SET

    paid=?,
    remaining=?,
    status=?

    WHERE id=?
    ''',
    (
    paid,
    remaining,
    status,
    id
    )
    )

    con.commit()

    con.close()

    return redirect("/fees")
@app.route("/events",methods=["GET","POST"])
def events():

    con=connect()
    cur=con.cursor()

    if request.method=="POST":

        cur.execute(
        '''
        INSERT INTO events(
        eventname,
        participants)
        VALUES(?,?)
        ''',
        (
        request.form["eventname"],
        request.form["participants"]
        )
        )

        con.commit()

    cur.execute(
    "SELECT * FROM events"
    )

    data=cur.fetchall()

    intersection=set()
    difference=set()
    union=set()

    if len(data)>=2:

        a=set(
        data[-2][2].split(",")
        )

        b=set(
        data[-1][2].split(",")
        )

        intersection=a&b

        difference=a-b

        union=a|b

    con.close()

    return render_template(
    "events.html",
    events=data,
    intersection=intersection,
    difference=difference,
    union=union
    )

@app.route("/delete_event/<id>")
def delete_event(id):

    con=connect()
    cur=con.cursor()

    cur.execute(
    "DELETE FROM events WHERE id=?",
    (id,)
    )

    con.commit()
    con.close()

    return redirect("/events")

app.run(debug=True)