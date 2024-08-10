from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Ensure this line is present

    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints/routes
    from . import routes
    app.register_blueprint(routes.bp)

    return app
