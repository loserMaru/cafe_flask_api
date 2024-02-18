from flask_restx import Api

api = Api(version='1.0', title='Cafe Flask Api', description='Swagger documentation for cafe app',
          doc='/docs/', authorizations=
          {'jwt': {
              'type': 'apiKey',
              'in': 'header',
              'name': 'Authorization',
              'description': 'JWT authorization, e.g. "token"'
          }
          })

# Очистка default namespace
api.namespaces.clear()

# Инициализация пространства имен для API
api_namespace = api.namespace('api', description='API operations', doc='')
login_namespace = api.namespace('Login', description='JWT-token receiving', path='/login')
user_namespace = api.namespace('Users', description='Users operations', path='/user', doc='')

