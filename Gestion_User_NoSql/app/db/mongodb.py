from pymongo import MongoClient, errors

class MongoDB:
    MONGO_URI = "mongodb+srv://sidydiopbalde:Toubakhayra@clustergestionuserpytho.qm3bwmd.mongodb.net/etablissement?retryWrites=true&w=majority&appName=ClusterGestionUserPython"

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
