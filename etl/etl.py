

class MessageBrocker:
    def __init__(self, client):
        self.client = client

class Database:
    def __init__(self, client):
        self.client = client

class ETL:
    def __init__(self, message_brocker:MessageBrocker, database: Database):
        pass


app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)