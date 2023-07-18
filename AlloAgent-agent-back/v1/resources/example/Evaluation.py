# pylint: disable=invalid-name
# pylint: disable=line-too-long
#imports python base
import json
import sys
import logging
#import terceros
from flask import session, jsonify, request
from flask_restful import Resource, reqparse
from mongoengine.context_managers import switch_db
from bson.json_util import dumps, loads
from datetime import datetime, timezone

#Import del sistema
from v1.resources.auth.authorization import Auth
from v1.resources.auth.dbDecorator import dbAccess
from v1.models.api_models import Evaluacion

logger = logging.getLogger(__name__)

class EvaluacionAll(Resource):
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    
    def get(self):
        with switch_db(Evaluacion, session["dbMongoEngine"]):
            my_model = Evaluacion.objects()
            if my_model:
                return jsonify(my_model.to_json())
        return "Objeto no encontrado", 400

class EvaluacionDetail(Resource):
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    
    def get(self):
        args = request.args
        folio = args.get('folio')
        pline = [
        {
            '$match': {
                'agente': 'Marcela Garay',
                'MT_Folio': folio,
            }
        }, {
            '$project': {
                'MT_Folio': '$MT_Folio',
                'campania': '$campania', 
                'encontrado': '$encontrado', 
                'id_cat': '$id_cat', 
                'id_sub': '$id_sub', 
                'categoria': '$categoria',
                'subcategoria': '$subcategoria',
                'elemento_explicito': '$elemento_explicito', 
                'puntaje': '$puntaje', 
                'audio': '$audio'
            }
        }, {
            '$group': {
                '_id': {
                    'MT_Folio': '$MT_Folio',
                    'campania': '$campania', 
                    'id_cat': '$id_cat', 
                    'id_sub': '$id_sub', 
                    'categoria': '$categoria',
                    'subcategoria': '$subcategoria',
                    'elemento_explicito': '$elemento_explicito', 
                    'audio': '$audio'
                }, 
                'TotalPuntaje': {
                    '$sum': '$puntaje'
                }, 
                'PuntajeObtenido': {
                    '$sum': {
                        '$multiply': [
                            '$encontrado', '$puntaje'
                        ]
                    }
                }
            }
        }, {
            '$addFields': {
                'Ponderacion': {
                    '$multiply': [
                        {
                            '$divide': [
                                '$PuntajeObtenido', '$TotalPuntaje'
                            ]
                        }, 100
                    ]
                }, 
                'Encontrado': {
                    '$cond': [
                        {
                            '$gt': [
                                '$PuntajeObtenido', 0
                            ]
                        }, 'SI', 'NO'
                    ]
                }
            }
        }, {
            '$sort': {
                '_id.id_cat': 1, 
                '_id.id_sub': 1
            }
        }
        ]
        with switch_db(Evaluacion, session["dbMongoEngine"]):
            my_model = Evaluacion.objects().aggregate(pipeline = pline)
            list_cur = list(my_model)
            if my_model:
                return list_cur
        return "Objeto no encontrado", 400

class EvaluacionGET(Resource):
    
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def get(self):
        args = request.args
        campania = args.get('campania')
        format = '%Y-%m-%d'
        date1 = str(args.get('fechai'))
        date2 = str(args.get('fechaf'))
        fechai = datetime.strptime(date1, format)
        fechaf = datetime.strptime(date2, format)
        if campania == 'Todos':
            pline = [
            {
                '$match': {
                    'agente': 'Marcela Garay', 
                    'FechaGestion': {
                        '$gt': fechai, 
                        '$lt': fechaf
                    }
                }
            }, {
                '$project': {
                    'MT_Folio': '$MT_Folio', 
                    'FechaGestion': {
                        '$dateToString': {
                            'format': format, 
                            'date': '$FechaGestion'
                        }
                    }, 
                    'campania': '$campania', 
                    'encontrado': '$encontrado', 
                    'id_cat': '$id_cat', 
                    'categoria': '$categoria', 
                    'puntaje': '$puntaje', 
                    'audio': '$audio'
                }
            }, {
                '$group': {
                    '_id': {
                        'MT_Folio': '$MT_Folio', 
                        'FechaGestion': '$FechaGestion', 
                        'campania': '$campania', 
                        'id_cat': '$id_cat', 
                        'categoria': '$categoria', 
                        'audio': '$audio'
                    }, 
                    'TotalPuntaje': {
                        '$sum': '$puntaje'
                    }, 
                    'PuntajeObtenido': {
                        '$sum': {
                            '$multiply': [
                                '$encontrado', '$puntaje'
                            ]
                        }
                    }
                }
            }, {
                '$addFields': {
                    'Ponderacion': {
                        '$multiply': [
                            {
                                '$divide': [
                                    '$PuntajeObtenido', '$TotalPuntaje'
                                ]
                            }, 100
                        ]
                    }
                }
            }, {
                '$sort': {
                    '_id.MT_Folio': -1, 
                    '_id.id_cat': 1
                }
            }
            ]
        else:
            pline = [
            {
                '$match': {
                    'agente': 'Marcela Garay',
                    'campania': campania,
                    'FechaGestion': {
                        '$gt': fechai, 
                        '$lt': fechaf
                    }
                }
            }, {
                '$project': {
                    'MT_Folio': '$MT_Folio', 
                    'FechaGestion': {
                        '$dateToString': {
                            'format': format, 
                            'date': '$FechaGestion'
                        }
                    }, 
                    'campania': '$campania', 
                    'encontrado': '$encontrado', 
                    'id_cat': '$id_cat', 
                    'categoria': '$categoria', 
                    'puntaje': '$puntaje', 
                    'audio': '$audio'
                }
            }, {
                '$group': {
                    '_id': {
                        'MT_Folio': '$MT_Folio', 
                        'FechaGestion': '$FechaGestion', 
                        'campania': '$campania', 
                        'id_cat': '$id_cat', 
                        'categoria': '$categoria', 
                        'audio': '$audio'
                    }, 
                    'TotalPuntaje': {
                        '$sum': '$puntaje'
                    }, 
                    'PuntajeObtenido': {
                        '$sum': {
                            '$multiply': [
                                '$encontrado', '$puntaje'
                            ]
                        }
                    }
                }
            }, {
                '$addFields': {
                    'Ponderacion': {
                        '$multiply': [
                            {
                                '$divide': [
                                    '$PuntajeObtenido', '$TotalPuntaje'
                                ]
                            }, 100
                        ]
                    }
                }
            }, {
                '$sort': {
                    '_id.MT_Folio': -1, 
                    '_id.id_cat': 1
                }
            }
            ]
        with switch_db(Evaluacion, session["dbMongoEngine"]):
            my_model = Evaluacion.objects().aggregate(pipeline = pline)
            list_cur = list(my_model)
            if list_cur == []:
                list_cur = [{
                    '_id': 
                    {'MT_Folio': '', 
                        'FechaGestion': '', 
                        'campania': '', 
                        'id_cat': '', 
                        'categoria': '', 
                        'audio': ''}, 
                    'TotalPuntaje': 0, 
                    'PuntajeObtenido': 0, 
                    'Ponderacion': 0
                    }]
            if my_model:
                return list_cur
        return "Objeto no encontrado", 400
    
class CampaniaGET(Resource):
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    
    def get(self):
        pline = [
        {
            '$match': {
                'agente': 'Marcela Garay'
            }
        }, {
            '$unwind': {
                'path': '$campania', 
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$group': {
                '_id': None, 
                'distinctcampanias': {
                    '$addToSet': '$campania'
                }
            }
        }
        ]
        with switch_db(Evaluacion, session["dbMongoEngine"]):
            my_model = Evaluacion.objects().aggregate(pipeline = pline)
            list_cur = list(my_model)
            if my_model:
                return list_cur
        return "Objeto no encontrado", 400

class TipoLlamadaGET(Resource):
    @Auth.authenticate
    @dbAccess.mongoEngineAccess

    def get(self):
        pline = [
            {
                '$match': {
                    'agente': 'Marcela Garay'
                }
            }, {
                '$group': {
                    '_id': {
                        'tipo_llamada': '$tipo_llamada'
                    }, 
                    'Total': {
                        '$sum': 1
                    }
                }
            }
        ]
        with switch_db(Evaluacion, session["dbMongoEngine"]):
            my_model = Evaluacion.objects().aggregate(pipeline = pline)
            list_cur = list(my_model)
            if my_model:
                return list_cur
        return "Objeto no encontrado", 400
    
class CardsGET(Resource):
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    
    def get(self):
        pline = [
            {
                '$match': {
                    'agente': 'Marcela Garay'
                }
            }, {
                '$group': {
                    '_id': {
                        'MT_Folio': '$MT_Folio', 
                        'id_cat': '$id_cat', 
                        'categoria': '$categoria'
                    }, 
                    'Total': {
                        '$sum': 1
                    }, 
                    'TotalPuntaje': {
                        '$sum': '$puntaje'
                    }, 
                    'PuntajeObtenido': {
                        '$sum': {
                            '$multiply': [
                                '$encontrado', '$puntaje'
                            ]
                        }
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'id_cat': '$_id.id_cat', 
                        'categoria': '$_id.categoria'
                    }, 
                    'Total': {
                        '$sum': 1
                    }, 
                    'TotalPuntaje': {
                        '$sum': '$TotalPuntaje'
                    }, 
                    'PuntajeObtenido': {
                        '$sum': '$PuntajeObtenido'
                    }
                }
            }, {
                '$addFields': {
                    'Promedio': {
                        '$multiply': [
                            {
                                '$divide': [
                                    '$PuntajeObtenido', '$TotalPuntaje'
                                ]
                            }, 100
                        ]
                    }
                }
            }, {
                '$sort': {
                    '_id.id_cat': 1
                }
            }
        ]
        
        with switch_db(Evaluacion, session["dbMongoEngine"]):
            my_model = Evaluacion.objects().aggregate(pipeline = pline)
            list_cur = list(my_model)
            if my_model:
                return list_cur
        return "Objeto no encontrado", 400
    
class ChartsGET(Resource):
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    
    def get(self):
        args = request.args
        id_cat = args.get('id_cat')
        
        pline = [
        {
            '$match': {
                'agente': 'Marcela Garay',
                'id_cat': id_cat,
            }
        }, {
            '$group': {
                '_id': {
                    'id_sub': '$id_sub',
                    'categoria': '$categoria',
                    'subcategoria': '$subcategoria',
                }, 
                'TotalPuntaje': {
                    '$sum': '$puntaje'
                }, 
                'PuntajeObtenido': {
                    '$sum': {
                        '$multiply': [
                            '$encontrado', '$puntaje'
                        ]
                    }
                }
            }
        }, {
            '$addFields': {
                'Promedio': {
                    '$multiply': [
                        {
                            '$divide': [
                                '$PuntajeObtenido', '$TotalPuntaje'
                            ]
                        }, 100
                    ]
                }
            }
        }, {
            '$sort': {
                '_id.id_cat': 1, 
                '_id.id_sub': 1
            }
        }
    ]
        
        with switch_db(Evaluacion, session["dbMongoEngine"]):
            my_model = Evaluacion.objects().aggregate(pipeline = pline)
            list_cur = list(my_model)
            if my_model:
                return list_cur
        return "Objeto no encontrado", 400
