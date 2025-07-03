from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

# Use PyMySQL as MySQLdb driver
import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder="static")
    app.config["SECRET_KEY"] = "change_this_in_prod"

    # ✅ Update these values with your MySQL setup
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://seguser:StrongPassword123@localhost:3306/customer_segmentation"
    )


    # Upload destination (for CSV and plot files)
    app.config["UPLOAD_FOLDER"] = Path(__file__).parent / "static" / "uploads"
    app.config["UPLOAD_FOLDER"].mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    # Register blueprints
    from .routes_auth import auth_bp
    from .routes_main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
