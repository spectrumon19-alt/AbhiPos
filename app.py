import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__, static_folder='.')
    CORS(app)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.products import products_bp
    from routes.sales import sales_bp
    from routes.inventory import inventory_bp
    from routes.reports import reports_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(sales_bp, url_prefix='/api')
    app.register_blueprint(inventory_bp, url_prefix='/api')
    app.register_blueprint(reports_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    
    # Initialize database
    from db import init_db
    with app.app_context():
        init_db()
    
    # Serve static files
    @app.route('/')
    def index():
        return send_from_directory('.', 'start.html')
    
    @app.route('/<path:filename>')
    def static_files(filename):
        return send_from_directory('.', filename)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5001)