

class MessageBrocker:
    def __init__(self, client):
        self.client = client

class Database:
    def __init__(self, client):
        self.client = client

class ETL:
    def __init__(self, message_brocker:MessageBrocker, database: Database):
        pass



if __name__ == "__main__":
    pass