from flask import Flask

CONFIG_NAME_MAPPER = {
    "development": "config.DevelopmentConfig",
    "testing": "config.TestingConfig",
    "production": "config.ProductionConfig",
}


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = "development"

    app.config.from_object(CONFIG_NAME_MAPPER[config_name])

    # Register extensions
    from extensions import db, cors, ma
    db.init_app(app)
    cors.init_app(app)
    ma.init_app(app)

    # Register Blueprints
    from api.tracks import api_tracks_bp
    app.register_blueprint(api_tracks_bp, url_prefix="/api/v1")

    return app
