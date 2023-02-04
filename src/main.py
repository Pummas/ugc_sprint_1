import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.post('/load_data')
async def load_data(data: dict):
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)




