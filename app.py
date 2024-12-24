import logging

import uvicorn
from fastapi import FastAPI

from routing.review import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, log_level="debug", port=8080)
