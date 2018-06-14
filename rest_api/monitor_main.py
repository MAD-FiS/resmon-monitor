# --coding=utf-8--
import connexion

import swagger_server.encoder

connApp = connexion.App(__name__,
                        specification_dir='./swagger_server/swagger/')
connApp.add_api(
    'swagger.yaml',
    arguments={'title': 'ResMon - monitorowanie rozproszonych zasobów'})
app = connApp.app

# def main():
#     app.app.json_encoder = encoder.JSONEncoder
#     app.run(port=8080)


# if __name__ == '__main__':
#     main()
