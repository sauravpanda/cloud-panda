from flask import Blueprint, render_template, request, redirect, url_for
from models import Task, tasks

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@routes_bp.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        assignee = request.form['assignee']
        task = Task(title, description, assignee)
        tasks.append(task)
        return redirect(url_for('routes.index'))
    return render_template('create_task.html')

@routes_bp.route('/task/<int:task_id>')
def task_details(task_id):
    task = tasks[task_id]
    return render_template('task_details.html', task=task)

@routes_bp.route('/task/<int:task_id>/complete')
def complete_task(task_id):
    task = tasks[task_id]
    task.mark_completed()
    return redirect(url_for('routes.index'))