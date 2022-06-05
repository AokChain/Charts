from flask_caching import Cache
from flask_cors import CORS
from flask import Flask
from .models import db
import config

db.bind(**config.db)
db.generate_mapping(create_tables=True)

cache = Cache(config={"CACHE_TYPE": "simple"})

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.secret
    cache.init_app(app)
    CORS(app)

    with app.app_context():
        from .chart import chart
        from .stats import stats

        app.register_blueprint(chart)
        app.register_blueprint(stats)

        return app
