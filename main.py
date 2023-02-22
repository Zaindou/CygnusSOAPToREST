from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services import soap_cygnus
import json
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.get('/api/credito')
async def root(request: Request):

    body = await request.body()

    data = json.loads(body.decode("utf-8"))
    
    identificacion = data["identificacion"]
    num_radicado = data["num_radicado"]
    
    response_json = soap_cygnus(identificacion, num_radicado)

    parsed_response = json.loads(response_json)

    return JSONResponse(parsed_response)



if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
