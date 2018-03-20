#! /usr/bin/env python3.6
# @author anton.belyaev@bostongene.com
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import g


manager = Manager(g.app)
migrate = Migrate(g.app, g.db)

# run database migrations and upgrades
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
