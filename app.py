import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Task {self.title}>'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            task_title = request.form.get('task')
            due_date = request.form.get('due_date')
            if due_date:  # Convert the string to datetime if present
                due_date = datetime.fromisoformat(due_date)
            print(f"Adding new task: {task_title} with due date: {due_date}")
            new_task = Task(title=task_title, due_date=due_date)
            db.session.add(new_task)
            db.session.commit()
            print("Task added successfully")
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while adding task: {e}")
        return redirect('/')
    else:
        tasks = Task.query.order_by(Task.id).all()
        print(f"Found {len(tasks)} tasks in database")
        for task in tasks:
            print(
                f"Task: {task.title}, Due: {task.due_date}, Completed: {task.completed}")
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {e}")
    return redirect('/')


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        try:
            # Changed from 'task' to 'title' to match form
            task.title = request.form.get('title')
            due_date = request.form.get('due_date')
            if due_date:  # Convert the string to datetime if present
                task.due_date = datetime.fromisoformat(due_date)
            else:
                task.due_date = None
            task.completed = request.form.get('completed') == 'on'
            db.session.commit()
            print(f"Task updated successfully: {task.title}")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating task: {e}")
        return redirect('/')
    return render_template('edit.html', task=task)
    return render_template('edit.html', task=task)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
