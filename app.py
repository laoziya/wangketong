
from flask import Flask
import os

def create_app(config=None):
    app = Flask(__name__)
    # 加载config配置
    #app.config类继承了dict
    app.config.from_object('config.settings')

    if 'FLASK_CONF' in os.environ:
        app.config.from_envvar('FLASK_CONF')


    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    # 绑定蓝图
    import router
    router.init_app(app)
    # 绑定sql模型
    import model
    model.init_app_db(app)
    return app
