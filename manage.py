#!/usr/bin/env python
# coding=utf8

"""
create on 2017-10-11
@author: cao kun
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from settings import app
from index.views import index_app
from test_demo.model import *
from project.model import *
from auth.model import *
from order.model import *

app.register_blueprint(index_app)

migrate = Migrate(app, db)
manage = Manager(app)
manage.add_command('db', MigrateCommand)


# @manage.command
# def create_db():
#     db.create_all()


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=9999, debug=app.debug)
    manage.run()
