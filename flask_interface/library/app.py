from flask import Flask

from flask_interface.library.settings import DevConfig


def create_app(db, config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from flask_interface.library.books import views
    app.register_blueprint(views.blueprint)
    # app.register_blueprint(reader.blueprint)
    db.create_all(app=app)
    return app
