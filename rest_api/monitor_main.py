# --coding=utf-8--
import connexion

from swagger_server import encoder
from flask_jwt_extended import JWTManager

connApp = connexion.App(__name__,
                        specification_dir='./swagger_server/swagger/')
connApp.add_api(
    'swagger.yaml',
    arguments={'title': 'ResMon - monitorowanie rozproszonych zasobów'})
app = connApp.app
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

def main():
    app.json_encoder = encoder.JSONEncoder
    app.run(port=8080)


if __name__ == '__main__':
    main()
