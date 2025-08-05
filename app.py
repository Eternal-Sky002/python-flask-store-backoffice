from flask import Flask
from modules.user import user_bp
from modules.item import item_bp
from modules.store import store_bp
from modules.tag import tag_bp

def create_app():
        
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-here'

    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(tag_bp)

    return app