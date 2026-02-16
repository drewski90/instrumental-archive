from uploads import uploads_router
from auth import auth_router
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(
        __name__,
        static_url_path=""
    )
    app.config["UPLOAD_BUCKET"] = os.environ["UPLOAD_BUCKET"]
    app.config["STORAGE_BUCKET"] = os.environ["STORAGE_BUCKET"]
    app.config["TABLE_NAME"] = os.environ["TABLE_NAME"]
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")

    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True
    )

    app.register_blueprint(uploads_router, url_prefix="/api")
    app.register_blueprint(auth_router, url_prefix="/api")

    @app.route("/", defaults={"path": ""})
    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    return app

app = create_app()



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
