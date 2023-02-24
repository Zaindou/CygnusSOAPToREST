from dotenv import load_dotenv
from fastapi import Request
from fastapi.responses import JSONResponse
from serializer import serialize_response
from zeep import Client
from zeep.transports import Transport
from cachetools import TTLCache
import json
import os
import requests


load_dotenv()

# Cygnus soap enviroment variables
cygnus_soap_url = os.getenv('cygnus_soap_url')
db_name = os.getenv('db_name')
db_user = os.getenv('db_user')
db_password = os.getenv('db_password')

# BPM enviroment variables
bpm_url = os.getenv('bpm_url')
bpm_username = os.getenv('bpm_username')
bpm_password = os.getenv('bpm_password')


def soap_cygnus(identificacion, num_radicado):
    client = Client(cygnus_soap_url,
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


def get_token_bpm():

    urlRequest = f'{bpm_url}/Token/Authenticate'

    payload = json.dumps(
        {"UserName": bpm_username, "Password": bpm_password}
    )

    headers = {"Content-Type": "application/json"}

    response = requests.request(
        "POST", urlRequest, headers=headers, data=payload, verify=False)

    return response.text


def get_info_credito(id):

    token = get_token_bpm()

    url = f'{bpm_url}/cygnus/credit/' + id

    payload = {}
    headers = {
        "Authorization": "Bearer " + token,
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
    }

    response = requests.request(
        "GET", url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        return "Error, no se ha logrado procesar tu solicitud."


async def get_plandepagos(request: Request):

    body = await request.body()

    data = json.loads(body.decode("utf-8"))

    identificacion = data["identificacion"]
    num_radicado = data["num_radicado"]

    response_json = soap_cygnus(identificacion, num_radicado)

    parsed_response = json.loads(response_json)

    return JSONResponse(parsed_response)
