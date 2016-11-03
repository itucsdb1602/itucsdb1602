import psycopg2 as dbapi2

from news_class import news
from flask.globals import current_app

class newsService():
	def init_news_tbl(self):
		with dbapi2.connect(current_app.config['dsn']) as connection:
			cursor = connection.cursor()
			query = """CREATE TABLE news(
				id SERIAL PRIMARY KEY,
				headline TEXT UNIQUE NOT NULL,
				author TEXT NOT NULL,
				kind TEXT NOT NULL,
				)"""
			cursor.execute(query)
			connection.commit()
	def add_news(self, news):
		with dbapi2.connect(current_app.config['dsn']) as connection:
			cursor = connection.cursor()
			query = "INSET INTO news (headline, author, kind) VALUES (%s, %s, %s)"
			data = (news.headline, news.author, news.kind)
			cursor.execute(query, data)
			connection.commit()
	def delete_news(self, news):
		with dbapi2.connect(current_app.config['dsn']) as connection:
			cursor = connection.cursor()
			query = 'DELETE FROM news WHERE headline = %s'
			cursor.execute(query, news.headline)
			connection.commit()
	def get_news(self, news):
		with dbapi2.connect(current_app.config['dsn']) as connection:
			cursor = connection.cursor()
			query = "SELECT * FROM news WHERE headline = %s"
			cursor.execute(query, news.headline)
			connection.commit()
	def update_news(self, news):
		with dbapi2.connect(current_app.config['dsn']) as connection:
			cursor.connection.cursor()
			query = 'UPDATE news SET headline = %s, author = %s, kind = %s WHERE id = %s'
			data = (news[1].headline, news[1].author, news[1].kind, news[0].id)
			cursor.execute(query, data)
			connection.commit()


