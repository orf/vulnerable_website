from flask import Flask, g, render_template, abort, redirect, url_for, request, send_file
import sqlite3
import sys
import os
import base64

app = Flask(__name__)
app.config["SESSION_COOKIE_HTTPONLY"] = False
DATABASE = "site.db"


def connect_db():
    return sqlite3.connect(DATABASE)


def runQuery(query, args=tuple(), one=False):
    cursor = g.db.cursor()
    q = cursor.execute(query, args)
    if one:
        return q.fetchone()
    return q.fetchall()


def runInsert(query, args=tuple()):
    cursor = g.db.cursor()
    cursor.execute(query, args)
    g.db.commit()


@app.before_request
def before_request():
    g.db = connect_db()
    user_name = base64.decodestring(request.cookies.get("session", ""))

    if user_name:
        g.user = runQuery("SELECT * FROM users WHERE username = ?", (user_name,), one=True)
    else:
        g.user = None


@app.teardown_appcontext
def teardown_request(ex):
    if hasattr(g, "db"):
        g.db.close()


@app.route('/')
def index():
    some_products = runQuery('SELECT * FROM products LIMIT 3')
    return render_template("index.html", products=some_products)


@app.route("/logout")
def logout():
    r = redirect(url_for("index", message="You have been logged out"))
    r.set_cookie("session", "")
    return r


@app.route('/login', methods=["POST"])
def login():
    username, password = request.form["username"], request.form["password"]
    print password
    user = runQuery("SELECT * FROM users WHERE username = ? AND password = '%s'" % password,
                    (username,), one=True)
    message = "You have been logged in" if user else "Invalid login"

    resp = redirect(url_for("index", message=message))

    if user:
        resp.set_cookie("session", base64.encodestring(user[2]))

    return resp


@app.route('/search')
def search():
    if request.args.get("query"):
        search_results = runQuery("SELECT * FROM products WHERE lower(title) LIKE '%%%s%%'" % request.args.get("query"))
    else:
        search_results = None
    return render_template("search.html", search_results=search_results, query=request.args.get("query", None))


@app.route("/get_image")
def get_image():
    return send_file(request.args["path"])

@app.route("/product/<int:id>")
def view_product(id):
    product = runQuery("SELECT * FROM products WHERE id = ?", (id,), one=True)
    if product is None:
        return abort(404)
    comments = runQuery("SELECT * FROM comments WHERE product_id = ?", (product[0],))
    return render_template("product.html", product=product, comments=comments)


@app.route("/product/<int:id>/add_comment", methods=["POST"])
def add_comment(id):
    product = runQuery("SELECT * FROM products WHERE id = ?", (id,), one=True)
    if product is None:
        return abort(404)

    comment_text = request.form["comment"]
    runInsert("INSERT INTO comments (product_id, message) VALUES (?, ?)", (product[0], comment_text))

    return redirect(url_for("view_product", id=id, message="Comment added"))


def init_db():
    with app.app_context():
        if os.path.exists(DATABASE):
            os.remove(DATABASE)
        db = connect_db()
        with app.open_resource('sql/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        with app.open_resource('sql/initial_data.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == '__main__':
    if "initdb" in sys.argv:
        print "Creating DB"
        init_db()
    else:
        app.run()
