from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


# CONCEPT 2: Routes
@app.route("/")
def home():
    print("hi")
    select_query = db.select(Todo)
    todo_list = db.session.scalars(select_query).all()
    # CONCEPT 1: Polyglotism
    return render_template("base.html", todo_list=todo_list)


# CONCEPT 2: Routes
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    insert_query = db.insert(Todo)
    db_todo = {}
    db_todo["title"] = title
    db_todo["complete"] = False
    db.session.execute(insert_query, db_todo)
    db.session.commit()
    return redirect(url_for("home"))


# CONCEPT 2: Routes
@app.route("/update/<int:todo_id>")
def update(todo_id):
    select_query = db.select(Todo).where(Todo.id == todo_id)
    todo = db.session.scalars(select_query).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


# CONCEPT 2: Routes
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    delete_query = db.delete(Todo).where(Todo.id == todo_id)
    db.session.execute(delete_query)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)