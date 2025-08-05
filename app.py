from flask import Flask
from modules.user import user_bp
from modules.item import item_bp
from modules.store import store_bp
from modules.tag import tag_bp

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(item_bp)
app.register_blueprint(store_bp)
app.register_blueprint(tag_bp)

if __name__ == '__main__':
    app.run(debug=True, port=8001)