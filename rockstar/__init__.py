from flask import Flask
from rockstar.config import Config
from rockstar import routes


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register blueprints here
    app.register_blueprint(routes.bp)

    @app.route('/test/')
    def test_page():
        return 'hello'

    return app
