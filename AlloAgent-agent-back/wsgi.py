import eventlet
eventlet.monkey_patch()

from flask_restful import Api #importamos la libreria para crear recursos REST
from flask_cors import CORS #biblioteca para configurar cors
from config import app #de aqui se obtienen configuraciones
from v1.resources.routes import initialize_routes #importamos las rutas

# Flask restful con errores personalizados
CORS(app) #configuramos cors
api = Api(app) #instanciamos el api

initialize_routes(api) #inicializamos las rutas
