#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from flask_script.commands import Clean, ShowUrls
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from repo.Flask_Alchemy.database import db

from flask_interface.library.app import create_app

app = create_app(db)
manager = Manager(app)

manager.add_command('server', Server())
manager.add_command('urls', ShowUrls())
manager.add_command('clean', Clean())

if __name__ == '__main__':
    manager.run()
