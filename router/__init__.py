from .study import stu_bp
from .root import root_bp
from .user_router import user_bp
from .course_router import course_bp


def init_app(app):
    app.register_blueprint(stu_bp)
    app.register_blueprint(root_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(course_bp)
    # app.register_blueprint(stu_user_bp)