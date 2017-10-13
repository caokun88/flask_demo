#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-11
@author: cao kun
"""

from flask import send_from_directory

from settings import app, static_dir
from index.views import index_app
from test_demo.views import test_app
from project.views import project_app

app.register_blueprint(index_app)
app.register_blueprint(test_app, url_prefix='/test')
app.register_blueprint(project_app, url_prefix='/project')


if __name__ == '__main__':

    @app.route('/static/<path:filename>')
    def show_file(filename):
        print filename
        return send_from_directory(static_dir, filename)
    app.run(host='0.0.0.0', port=5000, debug=app.debug)
