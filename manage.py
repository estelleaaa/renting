# manage.py 作为启动文件 仅反应启动的流程 只需求把flask程序启动起来即可

from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# 创建flask应用对象
app = create_app("develop")

manager = Manager(app)

Migrate(app, db)

manager.add_command("db", MigrateCommand)
if __name__ == '__main__':
    manager.run()