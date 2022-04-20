from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('cs324.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM event ORDER BY id")
    calendar = cur.fetchall()
    print(calendar)
    return render_template('calendar.html', calendar=calendar)


@app.route("/insert", methods=["POST", "GET"])
def insert():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        print(title)
        print(start)
        cur.execute(
            'INSERT INTO event (title,start_event) values (?,?)',
            (title, start)
        )
        conn.commit()
        cur.close()
        msg = 'success'
    return jsonify(msg)


@app.route("/update", methods=["POST", "GET"])
def update():
    conn = get_db_connection();
    cur = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        id = request.form['id']
        print(title)
        print(start)
        print(id)
        cur.execute("UPDATE event SET title = ?, start_event = ? WHERE id = ? ",
                    [title, start, id])
        conn.commit()
        cur.close()
        msg = 'success'
    return jsonify(msg)


@app.route("/delete", methods=["POST", "GET"])
def ajax_delete():
    conn = get_db_connection();
    cur = conn.cursor()
    if request.method == 'POST':
        getid = request.form['id']
        print(getid, "ID")
        cur.execute('DELETE FROM event WHERE id = {0}'.format(getid))
        conn.commit()
        cur.close()
        msg = 'Record deleted successfully'
    return jsonify(msg)


if __name__ == '__main__':
    app.run()
