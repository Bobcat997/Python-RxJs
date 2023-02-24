from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "Data.db"


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


@app.route('/tasks', methods=['POST'])
def create_task():
    task_data = request.get_json()
    if not task_data or not task_data.get('title'):
        return jsonify({'error': 'Title is required.'}), 400

    new_task = {
        'title': task_data['title'],
        'description': task_data.get('description', ''),
        'done': False
    }

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO tasks (title, description, done) VALUES (?, ?, ?)',
                   (new_task['title'], new_task['description'], new_task['done']))
    db.commit()
    cursor.close()
    db.close()

    new_task['id'] = cursor.lastrowid

    return jsonify({'task': new_task}), 201


@app.route('/tasks', methods=['GET'])
def list_tasks():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    cursor.close()
    db.close()
    response_data = [{"id": task[0], "title": task[1], "description": task[2], "done": task[3]} for task in tasks]
    return jsonify(response_data), 200


@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    task_data = request.get_json()
    if not task_data:
        return jsonify({'error': 'Request body is required.'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()

    if not task:
        return jsonify({'error': 'Task not found.'}), 404

    updated_task = {
        'title': task_data.get('title', task['title']),
        'description': task_data.get('description', task['description']),
        'done': task_data.get('done', task['done'])
    }

    cursor.execute('UPDATE tasks SET title = ?, description = ?, done = ? WHERE id = ?',
                   (updated_task['title'], updated_task['description'], updated_task['done'], task_id))
    db.commit()
    cursor.close()
    db.close()

    updated_task['id'] = task_id

    return jsonify({'task': updated_task})


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({'result': True})


if __name__ == "__main__":
    app.run(debug=True)
