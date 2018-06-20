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
        with open("/app/jwt.key") as f:
            key = f.read().rstrip()
    except FileNotFoundError:
        print(
            'File with authorization key "jwt.key" not found',
            "Monitor is unable to start",
        )
        sys.exit(
            'File with authorization key "jwt.key" not found.'
            "Monitor is unable to start"
        )

    # connApp.app.config["JWT_SECRET_KEY"] = key
    connApp.app.config['JWT_SECRET_KEY'] = \
        'eea637dfa8c5da0db6740b4b5708ee7aecc1d5f9f830d1ce7ab9df480bace474d8db8484b84ee'\
        '4b16e8fbb490e0ac519caaec508379622abe051ba2a9dcda431'
    jwt = JWTManager(connApp.app)

    return connApp.app(environ, start_fn)
