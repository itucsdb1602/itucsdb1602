import datetime
import os
import json
import re
import psycopg2 as dbapi2

from flask import Flask
from flask import render_template
import flask_login
from tag_handler import tag
from announcement_handler import announcement
from post_like_handler import pLikes
from user_handler import user
from user_block_handler import user_block
from user_friend_handler import user_friend
from keywords_handler import keywords
from post_handler import post
from group_handler import group
from comments_handler import comment
from post_keywords_handler import pKeywordss
from user_subs_handler import uSubs

app = Flask(__name__)

app.secret_key = '7e6e814998ab3de2b63401a58063c79d92865d79'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.user_loader(user.service.get_user_by_id)
login_manager.login_view = "user.login"

app.register_blueprint(tag)
app.register_blueprint(announcement)
app.register_blueprint(pLikes)
app.register_blueprint(user)
app.register_blueprint(user_block)
app.register_blueprint(user_friend)
app.register_blueprint(keywords)
app.register_blueprint(post)
app.register_blueprint(group)
app.register_blueprint(comment)
app.register_blueprint(pKeywordss)
app.register_blueprint(uSubs)



def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/')
def home_page():
    try:
        all_tags = tag.service.get_all_tags()
    except dbapi2.Error as e:
        all_tags = None
    try:
        all_posts = post.service.get_all_posts()
        for post_id, postObj in all_posts:
            postObj.post_like = pLikes.service.get_all_post_like(post_id)
            postObj.comment_counter = comment.service.get_comment_counter(post_id)
    except dbapi2.Error as e:
        all_posts = None
    return render_template('home.html', all_tags=all_tags, all_posts = all_posts)

@app.route('/groups')
def group_page():
    return render_template('groups.html')
@app.route('/announcements')
def announcement_page():
    return render_template('announcements.html')


@app.route('/hakan')
def hakan_page():
    return render_template('hakan.html')

@app.route('/gokturk')
def gokturk_page():
    return render_template('gokturk.html')
@app.route('/bilal')
def bilal_page():
    return render_template('bilal.html')
@app.route('/samet')
def samet_page():
    return render_template('samet.html')

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)
