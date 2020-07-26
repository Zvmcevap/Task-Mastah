from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime


# Set app and database variable
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

# SQL Alchemy database model, needs a review
# Class of an Task featuring its data
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<test %r>' % self.id


# Application innards and stuff :S
@app.route('/', methods=['POST', 'GET'])
def index():
    current_user = "Anonymous"
    # When submitting a new task this happens
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"

    else:
        # Tasks will return all the tasks from the db in the order they were created
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks, current_user=current_user)


# PLACEHOLDERS for callendar, log-in/out!!!!!!!!!
@app.route('/calendar/')
def calendar():
    return render_template('create_task.html')


@app.route('/')
def login():
    return redirect('/')


@app.route('/')
def logout():
    return redirect('/')


# Delete the particular task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'Problem deleting that task'


# Update the particular task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:

            db.session.commit()
            return redirect('/')

        except:
            return "Problem updating that task"

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
