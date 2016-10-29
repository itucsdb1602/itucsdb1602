import psycopg2 as dbapi2
from flask import Blueprint, render_template, jsonify
from flask.globals import current_app, request
from tag_service import TagService
from tag_class import Tag
from crypt import methods

tag = Blueprint('tag',__name__)
tag.service = TagService()

@tag.route('/tags/init')
def init_tag_database():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """CREATE TABLE tags (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )"""
        cursor.execute(query)
        connection.commit()

@tag.route('/tags/add', methods = ['GET', 'POST'])
def add_tag():
    if request.method == 'GET':
        return render_template('add_tag.html')
    else:
        tagObject = Tag(request.json['name'])
        tag.service.add_tag(tagObject)
        return jsonify({'status':'OK'});

