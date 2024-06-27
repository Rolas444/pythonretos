from flask import Blueprint

todo = Blueprint('todo', __name__)

@todo.get('/')
def list_todos():
    return 'List of todos'

@todo.post('/')
def create_todo():
    return 'Create a todo'

@todo.get('/<id>')
def get_todo(id):
    return f'Todo with id {id}'

@todo.put('/<id>')
def update_todo(id):
    return f'Update todo with id {id}'

@todo.delete('/<id>')
def delete_todo(id):
    return f'Delete todo with id {id}'