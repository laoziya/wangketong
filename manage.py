from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from model import db

app = create_app()
manager = Manager(app)

# 使用migrate管理app的数据模型变更
migrate = Migrate()
migrate.init_app(app, db)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()

