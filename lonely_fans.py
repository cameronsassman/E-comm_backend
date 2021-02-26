import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

def dict_factory(cursor,row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS Products '
                 '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                 'name TEXT, '
                 'character TEXT, '
                 'style TEXT, '
                 'gender TEXT, '
                 'colour TEXT, '
                 'size TEXT, '
                 'price TEXT, '
                 'description TEXT, '
                 'image TEXT)'
                 )
    print("Table created successfully")
    conn.close()

init_sqlite_db()

app = Flask(__name__)
CORS(app)

@app.route('/add-record/', methods=["POST"])
def add_new_record():
    if request.method == "POST":
        msg = None
        try:
            name = request.form['name']
            character = request.form['character']
            style = request.form['style']
            gender = request.form['gender']
            colour = request.form['colour']
            size = request.form['size']
            price = request.form['price']
            description = request.form['description']
            image = request.form['image']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Products (name, character, style, gender, colour, size, price, description, image) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (name, character, style, gender, colour, size, price, description, image))
                con.commit()
                msg = "Record successfully added."

        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            con.close()
            return jsonify(msg)

@app.route('/show-records/', methods=["GET"])
def show_records():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory=dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM Products")
            records = cur.fetchall()
    except Exception as e:
            con.rollback()
            print("There was an error fetching results from the database.")
    finally:
        con.close()
        return jsonify(records)

if __name__ == "__main__":
    app.run(debug=True)