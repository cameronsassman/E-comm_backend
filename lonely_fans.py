import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

def dict_factory(cursor,row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS Products'
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

@app.route('/test/')
def test():
    return render_template('test.html')

@app.route('/add-record/', methods=["POST"])
def add_new_record():
    if request.method == "POST":
        msg = None
        try:
            post_data = request.get_json()
            name = post_data['name']
            character = post_data['character']
            style = post_data['style']
            gender = post_data['gender']
            colour = post_data['colour']
            size = post_data['size']
            price = post_data['price']
            description = post_data['description']
            image = post_data['image']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Products"
                            "(name, character, style, gender, colour, size, price, description, image) "
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

@app.route('/show-records/',methods=["GET"])
def show_records():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM Products")
            records = cur.fetchall()
    except Exception as e:
            con.rollback()
            print("There was an error fetching results from the database.") + str(e)
    finally:
        con.close()
        return jsonify(records)

@app.route('/show-record-item/<int:product_id',methods=["GET"])
def show_record_item(product_id):
    record = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM Products WHERE id=" + str(product_id))
            record = cur.fetchone()
    except Exception as e:
            con.rollback()
            print("There was an error fetching results from the database.") + str(e)
    finally:
        con.close()
        return jsonify(record)


@app.route('/delete-record/<int:id>/', methods=['GET'])
def delete_product(id):

    msg = None

    try:
        with sqlite3.connect('database.db') as con:
            cur =con.cursor()
            cur.execute("DELETE FROM Products WHERE id=" + str(id))
            con.commit()
            msg = "Product was successfully deleted from table"
    except Exception as e:
        con.rollback()
        msg ="error occcured while deleting product" + str(e)
    finally:
        con.close()
        return (msg)


if __name__ == "__main__":
    app.run(debug=True)