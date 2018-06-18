import logging

import connexion
from flask_testing import TestCase

from rest_api.swagger_server.encoder import JSONEncoder
from flask_jwt_extended import JWTManager


class BaseTestCase(TestCase):
    def create_app(self):
        logging.getLogger("connexion.operation").setLevel("ERROR")
        app = connexion.App(__name__, specification_dir="../swagger/")
        app.app.json_encoder = JSONEncoder
        app.add_api("swagger.yaml")

        app.app.config["JWT_SECRET_KEY"] = "jwt-secret-string"
        jwt = JWTManager(app.app)

        return app.app
