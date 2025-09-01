from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to_do.db'
db = SQLAlchemy(app)


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
        task_title = request.form.get('task')
        due_date = request.form.get('due_date')
        new_task = Task(title=task_title, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    else:
        tasks = Task.query.order_by(Task.id).all()
        return render_template('index.html', tasks=tasks)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
