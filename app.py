
from flask import Flask, render_template, request, jsonify
import sqlite3
from flask_cors import CORS


def dict_fact(cursor, row,):
    d = {}
    for idx, col in enumerate(cursor,description):
        d[col[0]] = row[idx]
        return d

def init_sqlite_db():
    connection = sqlite3.connect('database.db')
    print("sucessfuly opened database")
    connection.execute(' CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, fname TEXT, uname TEXT, passw TEXT, email TEXT )')
    print('succesfully open table')
    connection.execute('CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY AUTOINCREMENT, uname TEXT, passw TEXT)')
    print("sucessfully created the table")
    connection.close()

init_sqlite_db()

app = Flask(__name__)
CORS(app)

@app.route('/add-now/',methods=['POST'])
def add_now():
    message = None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            fname = post_data['fname']
            uname = post_data['uname']
            passw = post_data['passw']
            email = post_data['email']


            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO accounts (fname, uname , passw, email) VALUES (?, ?, ?, ?)",(fname, uname, passw,email))
                cur.execute("INSERT INTO admin (uname, passw) VALUES ('admin','admin')",(uname, passw))
                con.commit()
                message = fname + "successfully created account"
        except Exception as e:
            con.rollback()
            message = "Error occured in insert operation:" + str(e)
        finally:
            con.close()
            return jsonify(message)




@app.route('/login-into-account/', methods=["GET"])
def log_into_account():
    records = []
    if request.method == "POST":
        message = None

        try:
            post_data = request.get_json()
            uname = post_data['uname']
            passw = post_data['passw']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                sql = "SELECT * FROM accounts WHERE uname = ? and passw = ?"
                cur.execute(sql,[uname,passw])
                records = cur.fetchall()
        except Exception as e:
            con.rollback()
            message = "Error occured while collecting data from db:" + str(e)
        finally:
            con.close()
            return jsonify(records)


@app.route('/accounts/', methods=["GET"])
def collect_accounts():
    records = []
    message = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            sql = "SELECT * FROM accounts"
            cur.execute(sql)
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        message = "Error occured while collecting data from db:" + str(e)
    finally:
        con.close()
        return jsonify(records)



if __name__ == '__main__':
    app.run(debug=True)

