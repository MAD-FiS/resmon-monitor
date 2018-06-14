# --coding=utf-8--
import connexion


def app(environ, start_fn):

    connApp = connexion.App(__name__,
                            specification_dir='./swagger_server/swagger/')
    connApp.add_api(
        'swagger.yaml',
        arguments={'title': 'ResMon - monitorowanie rozproszonych zasobów'})

    return connApp.app(environ, start_fn)
