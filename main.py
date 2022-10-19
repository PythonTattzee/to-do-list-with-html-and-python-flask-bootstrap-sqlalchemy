from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired
import datetime
from sqlalchemy import Column, DateTime


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = StringField("Body", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


##Cafe TABLE Configuration
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.name


db.create_all()


@app.route("/")
def home():
    tasks = Task.query.all()
    return render_template("index.html", all_tasks=tasks)


@app.route("/task/<int:task_id>", methods=["GET", "POST"])
def show_task(task_id):
    chosen_task = Task.query.get(task_id)
    return render_template("task.html", task=chosen_task)


@app.route("/add", methods=["GET", "POST"])
def add_new_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            body=form.body.data,
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)



@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task_to_delete = Task.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
