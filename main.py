import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles
from dotenv import load_dotenv

from views import home
from api import weather_api
from security import auth


api = fastapi.FastAPI()


def configure():
    configure_routing()
    configure_api_keys()


def configure_routing():    
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(weather_api.router)
    api.include_router(auth.router)

def configure_api_keys():
    load_dotenv()
    

if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=8000, host='127.0.0.1')
else:
    configure()

