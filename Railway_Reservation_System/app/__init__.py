"""
Flask Application Factory.
Configures database connectivity, SQLite PRAGMA hooks, and registers modular blueprints.
"""
from flask import Flask, render_template
from sqlalchemy import event
from sqlalchemy.engine import Engine
from app.config import Config
from app.extensions import db


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enforces SQLite Foreign Key constraints to match MySQL InnoDB transactional semantics."""
    try:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    except Exception:
        pass


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from app.routes.main_routes import main_bp
    from app.routes.train_routes import train_bp
    from app.routes.passenger_routes import passenger_bp
    from app.routes.booking_routes import booking_bp
    from app.routes.cancellation_routes import cancel_bp
    from app.routes.waitlist_routes import waitlist_bp
    from app.routes.report_routes import report_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(train_bp)
    app.register_blueprint(passenger_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(cancel_bp)
    app.register_blueprint(waitlist_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(admin_bp)

    # Custom template filters
    @app.template_filter('currency')
    def currency_filter(val):
        try:
            return f"₹{float(val):,.2f}"
        except (ValueError, TypeError):
            return f"₹{val}"

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html', error=str(e)), 500

    return app
