#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-11
@author: cao kun
"""


from settings import app
from index.views import index_app
from test_demo.views import test_app

app.register_blueprint(index_app)
app.register_blueprint(test_app, url_prefix='/test')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.debug)
