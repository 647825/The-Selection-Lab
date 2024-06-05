import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            done BOOLEAN NOT NULL CHECK (done IN (0, 1)),
            priority TEXT,
            due_date DATE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def update_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Add columns if they don't exist
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'user_id' not in columns:
        cursor.execute('ALTER TABLE tasks ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1')
        cursor.execute('PRAGMA foreign_keys = ON')
        cursor.execute('ALTER TABLE tasks ADD FOREIGN KEY (user_id) REFERENCES users(id)')
    
    if 'priority' not in columns:
        cursor.execute('ALTER TABLE tasks ADD COLUMN priority TEXT')
    
    if 'due_date' not in columns:
        cursor.execute('ALTER TABLE tasks ADD COLUMN due_date DATE')
    
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_password(username, password):
    user = get_user(username)
    if user and check_password_hash(user[2], password):
        return True
    return False

def add_task(user_id, title, description, priority, due_date):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (user_id, title, description, done, priority, due_date) VALUES (?, ?, ?, ?, ?, ?)', (user_id, title, description, 0, priority, due_date))
    conn.commit()
    conn.close()

def get_tasks(user_id, search='', status='', priority=''):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM tasks WHERE user_id = ?'
    params = [user_id]
    
    if search:
        query += ' AND (title LIKE ? OR description LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    if status == 'done':
        query += ' AND done = 1'
    elif status == 'not_done':
        query += ' AND done = 0'
    
    if priority:
        query += ' AND priority = ?'
        params.append(priority)
    
    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(task_id, done):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET done = ? WHERE id = ?', (done, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def get_task(task_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def edit_task(task_id, title, description, priority, due_date):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET title = ?, description = ?, priority = ?, due_date = ? WHERE id = ?', (title, description, priority, due_date, task_id))
    conn.commit()
    conn.close()
    
def get_user_by_id(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user
