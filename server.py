import datetime
import os
import json
import re
import psycopg2 as dbapi2

from flask import Flask
from flask import render_template
from tag_handler import tag
from announcement_handler import announcement


app = Flask(__name__)
app.register_blueprint(tag)
app.register_blueprint(announcement)

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
        return render_template('home.html', all_tags = None)
    return render_template('home.html',all_tags = all_tags)

@app.route('/hakan')
def hakan_page():
    return render_template('hakan.html')

@app.route('/gokturk')
def gokturk_page():
    return render_template('gokturk.html')

@app.route('/bilal')
def bilal_page():
    return render_template('bilal.html')
@app.route('/ozgun')
def ozgun_page():
    return render_template('ozgun.html')
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