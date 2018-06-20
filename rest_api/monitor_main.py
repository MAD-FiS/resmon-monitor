# --coding=utf-8--
import connexion
import sys

from flask_jwt_extended import JWTManager


def app(environ, start_fn):

    connApp = connexion.App(
        __name__, specification_dir="./swagger_server/swagger/"
    )
    connApp.add_api(
        "swagger.yaml",
        arguments={"title": "ResMon - monitorowanie rozproszonych zasobów"},
    )

    try:
        with open("../data/jwt.key") as f:
            key = f.read().rstrip()
    except FileNotFoundError:
        print(
            'File with authorization key "./data/jwt.key" not found',
            "Monitor is unable to start",
        )
        sys.exit(
            'File with authorization key "./data/jwt.key" not found.'
            "Monitor is unable to start"
        )

    connApp.app.config["JWT_SECRET_KEY"] = key
    jwt = JWTManager(connApp.app)

    return connApp.app(environ, start_fn)
