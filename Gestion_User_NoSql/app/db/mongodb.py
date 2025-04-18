from pymongo import MongoClient, errors

class MongoDB:
    MONGO_URI = "mongodb+srv://walonaynekh:walonaynekh@walonaynekh.zjohx.mongodb.net/?retryWrites=true&w=majority&appName=walonaynekh"
    def __init__(self):
        try:
            self.client = MongoClient(self.MONGO_URI)

            self.db = self.client["etablissement"]
        except errors.ConnectionFailure as e:
            print("Erreur de connexion à MongoDB :", e)
            raise

    def get_collection(self, collection_name):
        return self.db[collection_name]

mongodb = MongoDB()
