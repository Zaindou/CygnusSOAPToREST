from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from services import soap_cygnus
from utils import decode_token, process_credit_info, cache, SECRET_KEY, USERNAME, PASSWORD
import json
import jwt
import uvicorn

app = FastAPI()

security = HTTPBasic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.get("/")
def welcome():
    return "CygnusSOAP is running 1.0"


@app.post('/getToken')
async def get_token(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(
            status_code=401, detail='Invalid username or password')

    acces_token = jwt.encode(
        {"sub": credentials.username}, SECRET_KEY, algorithm="HS256")
    return {"access_token": acces_token, "token_type": "bearer"}


@app.get('/cygnus/info_general/{id}')
async def get_planpagosandinfo(id, username: str = Depends(decode_token)):

    if id in cache:
        info_credito = cache[id]
    else:
        info_credito = process_credit_info(id)
        cache[id] = info_credito

    identificacion = info_credito["documentoCliente"]
    num_radicado = id

    response_json = soap_cygnus(identificacion, num_radicado)

    plan_pagos = json.loads(response_json)

    response_data = {
        "info_credito": info_credito,
        "plan_pagos": plan_pagos
    }

    return JSONResponse(response_data)


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
