# import libraries
from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'

# initialise app
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def home():
    # home page- just the ID, Maker, Model, and Image URL
    sql = """
            SELECT Cars.CarID, Makers.MakerName, Cars.CarName, Cars.ImageURL
            FROM Cars, Makers
            WHERE Cars.MakerID = Makers.MakerID;
        """
    results = query_db(sql)
    return render_template("home.html", results=results)


@app.route('/car/<int:id>')
def Car(id):
    # just one car based on the id
    sql = """
            SELECT *
            FROM Cars, Makers
            WHERE Makers.MakerID = Cars.MakerID
            AND Cars.CarID = ?;
        """
    result = query_db(sql, (id, ), True)
    return render_template("car.html", car=result)


@app.route('/makers/')
def Makers():
    # get all the makers id, name, and image url
    sql = """
            SELECT MakerID, MakerName, MakerImageURL
            FROM Makers;
        """
    result = query_db(sql)
    return render_template("makers.html", results=result)


@app.route('/makers/<int:id>')
def Maker(id):
    # show all cars for a single maker
    sql = """
            SELECT Cars.CarID, Makers.MakerName, Cars.CarName, Cars.ImageURL
            FROM Cars, Makers
            WHERE Cars.MakerID = ?
            AND Cars.MakerID = Makers.MakerID;
        """
    results = query_db(sql, (id,))
    return render_template("makercars.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
