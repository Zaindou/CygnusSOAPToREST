from dotenv import load_dotenv
from serializer import serialize_response
from zeep import Client
from zeep.transports import Transport
import json
import os

load_dotenv()

db_name = os.getenv('db_name')
db_user= os.getenv('db_user')
db_password = os.getenv('db_password')

def soap_cygnus(identificacion, num_radicado):
    client = Client('http://35.227.68.50/WsSimuladorQnt_pruebas/WSSimuladorCreditoQnt.asmx?WSDL',
                    transport=Transport(timeout=10))


    params = {
        'pws_fecha_cal': '',
        'pws_identific': f'{identificacion}',
        'pws_num_radic': f'{num_radicado}',
        'pws_bd': db_name,
        'pws_usu': db_user,
        'pws_psw': db_password
    }

    response = client.service.liqCreditoval(**params)

    response_json = json.dumps(serialize_response(response), indent=4)
    
    return response_json

