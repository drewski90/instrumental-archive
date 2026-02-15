from uploads import uploads_router
from auth import auth_router
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)

    # Example config loading
    app.config["S3_BUCKET"] = os.getenv("S3_BUCKET")
    app.config["TABLE_NAME"] = os.getenv("TABLE_NAME")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    # Enable CORS
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},   # change to your domain later
        supports_credentials=True
    )

    # Register routers
    app.register_blueprint(uploads_router, url_prefix="/api")
    app.register_blueprint(auth_router, url_prefix="/api")

    # Health check
    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})
    
    @app.route('/')
    def index():
        return render_template("base.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
