#!/usr/bin/env python3

import connexion
from flask_jwt_extended import JWTManager
from swagger_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')

    app.app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    jwt = JWTManager(app.app)

    app.app.json_encoder = encoder.JSONEncoder
    app.add_api(
        "swagger.yaml",
        arguments={"title": "ResMon - distributed resources monitoring"},
    )
    app.run(port=8080)


if __name__ == "__main__":
    main()
