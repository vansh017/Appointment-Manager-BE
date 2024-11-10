import traceback

import uvicorn
from fastapi import FastAPI

from api import main_router
from core.api_logging import api_log
from settings import SERVER_HOST, SERVER_PORT

app = FastAPI()
app.include_router(main_router)



@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    try:
        api_log.info("server started")
        uvicorn.run("main:app", reload=True, host=SERVER_HOST, port=SERVER_PORT)
    except Exception as e:
        traceback.print_exc()