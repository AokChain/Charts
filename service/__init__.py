from flask_cors import CORS
from flask import Flask
from .models import db
import config

db.bind(**config.db)
db.generate_mapping(create_tables=True)

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.secret
    CORS(app)

    with app.app_context():
        from .chart import chart

        app.register_blueprint(chart)

        return app
