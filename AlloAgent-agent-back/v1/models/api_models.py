from datetime import date, datetime
from email.policy import default
from logging import RootLogger
from xmlrpc.client import DateTime
from mongoengine import Document, DynamicDocument
from mongoengine import StringField, IntField


class Model1(Document):
    name = StringField(max_length=30, required=True)
    lastname = StringField(max_length=30, required=True)
    document_type = StringField(max_length=30, required=True)
    document_number = IntField(max_length=30, required=True)
    rol = StringField(max_length=30, required=True)
    user = StringField(max_length=30, required=True)
    password = StringField(max_length=30, required=True)
    address = StringField(max_length=30, required=True)
    email = StringField(max_length=30, required=True)
    phone = IntField(max_length=30, required=True)
    
    

    # def __str__(self):
    #     return {self.name}
    # def __str__(self):
    #     return {self.lastname}
    # def __str__(self):
    #     return {self.user}
    # def __str__(self):
    #     return {self.adress}
    # def __str__(self):
    #     return {self.email}
    # def __str__(self):
    #     return {self.password}
    # def __str__(self):
    #     return {self.rol}
    # def __str__(self):
    #     return {self.document_type}
    # def __str__(self):
    #     return {self.document_number}
    # def __str__(self):
    #     return {self.phone}


class Model2(DynamicDocument):
    meta = {'collection': 'model2'}

class Evaluacion(Document):
    FechaAnalisis = StringField(max_length=30, required=True)#defaul=datetime.now
    FechaGestion = StringField(max_length=30, required=True)
    FechaSubida = StringField(max_length=30, required=True)
    IDScript = StringField(max_length=30, required=True)
    MT_Folio = StringField(max_length=30, required=True)
    agente = StringField(max_length=30, required=True)
    audio = StringField(max_length=100, required=True)
    campania = StringField(max_length=30, required=True)
    cat_weight = IntField()
    categoria = StringField(max_length=50, required=True)
    cliente = StringField(max_length=30, required=True)
    cod = StringField(max_length=30, required=True)
    elemento_explicito = StringField(max_length=50, required=True)
    encontrado = IntField()
    id_cat = StringField(max_length=30, required=True)
    id_sub = StringField(max_length=30, required=True)
    noencontrado = IntField()
    puntaje = IntField()
    subcat_weight = IntField()
    subcategoria = StringField(max_length=30, required=True)
    tipo_llamada = StringField(max_length=30, required=True)


    # def __str__(self):
    #     return {self.idDocument}