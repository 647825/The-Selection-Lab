from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import models

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

models.init_db()
models.update_db()

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @staticmethod
    def get(username):
        user = models.get_user(username)
        if user:
            return User(id=user[0], username=user[1])
        return None

@login_manager.user_loader
def load_user(user_id):
    user_data = models.get_user_by_id(user_id)
    if user_data:
        return User(id=user_data[0], username=user_data[1])
    return None

@app.route('/')
@login_required
def index():
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    tasks = models.get_tasks(current_user.id, search, status, priority)
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority')
    due_date = request.form.get('due_date')
    if title and description:
        models.add_task(current_user.id, title, description, priority, due_date)
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>')
@login_required
def update(task_id):
    done = request.args.get('done', type=int)
    models.update_task(task_id, done)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
@login_required
def delete(task_id):
    models.delete_task(task_id)
    return redirect(url_for('index'))

@app.route('/update_task/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority')
    due_date = request.form.get('due_date')
    models.edit_task(task_id, title, description, priority, due_date)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if models.verify_password(username, password):
            user = User.get(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not models.get_user(username):
            models.add_user(username, password)
            flash('Registration successful, please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
