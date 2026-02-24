import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    filter_type = request.args.get('filter', 'all')
    
    if filter_type == 'pending':
        tasks = Task.query.filter_by(completed=False).all()
    elif filter_type == 'completed':
        tasks = Task.query.filter_by(completed=True).all()
    else:
        tasks = Task.query.all()
    
    return render_template('index.html', tasks=tasks, filter=filter_type)

@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('content', '').strip()
    
    if content:
        db.session.add(Task(content=content))
        db.session.commit()
        
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    task = Task.query.get(id)
    task.content = request.form.get('content')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete(id):
    task = Task.query.get(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)