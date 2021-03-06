from flask import Blueprint, render_template, request, redirect, url_for
import datetime
from . import db


bp = Blueprint("todos", __name__)

@bp.route("/")
def index():
    """View for home page which shows list of to-do items."""

    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)

@bp.route("/completed_task", methods= ('GET', 'POST'))
def completed_task():
    """View for the indwx page to see completed tasks"""
    cur = db.get_db().cursor()
    cur.execute("""
     SELECT * FROM todos
     WHERE completed = 'True';""")
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)


@bp.route("/not_completed_task", methods= ('GET', 'POST'))
def not_completed_task():
    """View for index page to see uncompleted task"""
    cur = db.get_db().cursor()
    cur.execute("""
     SELECT * FROM todos
     WHERE completed = 'False';""")
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos=todos)

@bp.route("/items", methods = ('GET', 'POST'))
def form():
    """View for form page which allows you to add an item to your list"""
    if request.method == 'POST':
        item = request.form['items']
        dt = datetime.datetime.now()


        cur = db.get_db().cursor()
        cur.execute("""
         INSERT INTO todos (description, completed, created_at)
         VALUES (%s, %s, %s);
         """,
         (item,False,dt))
        db.get_db().commit()
        cur.close()

        return redirect(url_for('todos.index'))
    return render_template('form.html')

@bp.route("/completed/<id>")
def strike(id):
    """Mark an item as completed"""

    cur = db.get_db().cursor()
    cur.execute("""
    UPDATE todos SET completed = True
    WHERE id = %s;
    """,
        (id,))
    db.get_db().commit()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos = todos)

@bp.route("/delete/<id>")
def delete(id):
    """delete a task when done with it"""

    cur = db.get_db().cursor()
    cur.execute("""
    DELETE FROM todos
    WHERE id = %s;
    """,
        (id,))
    db.get_db().commit()
    cur.execute('SELECT * FROM todos')
    todos = cur.fetchall()
    cur.close()

    return render_template("index.html", todos = todos)
