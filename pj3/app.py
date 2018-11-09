# MANAGEMENT DATA THROUGH FILE

from flask import Flask, render_template, redirect, request
import psycopg2 as pg
import psycopg2.extras
import psycopg2.extensions
import csv

app = Flask(__name__)

# db_connect = pg.connect(
# # conn_str = pg.connect(
# # conn_str = pg_connection.connection(
#     dbname="soyoung",
#     user = "soyoung",
#     host = "127.0.0.1",
#     password = "soyoung"
# )

# conn_str = "dbname=soyoung"

# with open('students.csv','r',encoding='utf-8') as f:
#     rdr = csv.reader(f)
#     for line in rdr:
#         print(line)
#     print('//')

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    sid = request.form.get('sid')
    passwd = request.form.get('passwd')

    with open('students.csv','r',encoding='utf-8') as f:
        rdr = csv.reader(f)
        # for line in rdr:
        #     print(line)
        tmp = "none"
        for line in rdr:
            if line[0].startswith(sid) and line[1].startswith(passwd):
                return redirect(f"/{sid}")
                tmp = line[1]
                print("exists")
        return render_template("error.html",msg="Wrong ID/Password")
        # tmp = line[1] for line in rdr if line[0]==sid
        # print(tmp)

    # conn = pg.connect(conn_str)
    # cur = conn.cursor()
    # sql = f"SELECT sid, password FROM students WHERE sid='{sid}'"
    # print(sql)

    # cur.execute(sql) #sql execute
    # rows = cur.fetchall()
    # if(len(rows)!=1):
    #     return render_template('error.html',msg="Wrong ID")
    #
    # print(rows[0])
    # conn.close()
    # print("=======================")
    # print(f"{sid}, {passwd}")
    # print("=======================")
    # return redirect(f"/{sid}")

@app.route("/<sid>")
def portal(sid):
    # conn = pg.connect(conn_str)
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) #결과물이 딕셔너리 형태로
    # sql = f"select sid, sname, major_id, grade, tutor_id from students where sid='{sid}'"

    # print(sql)
    # cur.execute(sql)
    # rows = cur.fetchall()
    # conn.close()
    with open('students.csv','r',encoding='utf-8') as f:
        rdr = csv.reader(f)
        # tmp = 0
        for line in rdr:
            if line[0].startswith("admin"):
                with open('contacts.csv','r',encoding='utf-8') as c:
                    cc = csv.reader(c)
                    next(cc)
                    return render_template("portal_admin.html", stu_data = line, con_data = cc)

                # return render_template("portal_admin.html", stu_data = line)
            elif line[0].startswith(sid):
                return render_template("portal.html", stu_data = line)
    return render_template("error.html",msg="error01")
    # return render_template("portal.html", stu_data = rows[0])

@app.route("/<sid>/contacts/edit",methods=['POST', 'GET'])
def edit(sid):
    phoneNum = request.form.get('phone-num')
    print("phone number:",phoneNum)

    with open('contacts.csv','r',encoding='utf-8') as c:
        rdr = csv.reader(c)
        next(rdr)
        for line in rdr:
            if line[1]==phoneNum:
                return render_template("edit.html", con_data=line)
    return render_template("error.html",msg="error02")

@app.route("/<sid>/credits")
def credits(sid):
    conn = pg.connect(conn_str)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) #결과물이 딕셔너리 형태로
    sql = f"SELECT cl.name, cl.course_id, cl.year_open as year, cl.credit, cr.grade FROM class cl, creduts cr where cr.sid='{sid}' AND cl.class_id = cr.class_id"

    print(sql)
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        print(row)
    conn.close()
    return render_template("credits.html", credits=rows)

if __name__ == "__main__":
    app.run(debug=True)
