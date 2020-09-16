from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yamilperez@localhost:5432/todoapp'
db = SQLAlchemy(app)

# ---------------------------------------------------------
# Controller
#----------------------------------------------------------
class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

  def __repr__(self):
    return f'<Todo ID: {self.id}, Description: {self.description}>'

db.create_all()
# ---------------------------------------------------------
# Controller
#----------------------------------------------------------
@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description=description)
    print('description', todo.id)
    db.session.add(todo)
    db.session.commit()
    body['id'] = todo.id
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)



# ---------------------------------------------------------
# Render.
#----------------------------------------------------------
@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.all())