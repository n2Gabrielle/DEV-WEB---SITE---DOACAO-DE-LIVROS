import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from extensions import db
import models


PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    default_database = f"sqlite:///{Path(app.instance_path) / 'livros.db'}"
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-only-change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", default_database),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from routes import main

    app.register_blueprint(main)
    with app.app_context():
        models.db.create_all()

    @app.cli.command("init-db")
    def init_db():
        """Create the database tables."""
        db.create_all()
        print("Tabelas do banco criadas.")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
    )
