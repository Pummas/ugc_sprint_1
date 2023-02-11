import uvicorn
from ugc.src.api.v1 import routes

from ugc.src.config import app

app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
