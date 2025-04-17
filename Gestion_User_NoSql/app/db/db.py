from pymongo import MongoClient, errors


class MongoDBClient:
    def __init__(self, uri, db_name):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        """Établit la connexion à MongoDB."""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            print(f"Connexion réussie à la base de données MongoDB : {self.db_name}")
        except errors.ConnectionFailure as e:
            print("Erreur de connexion à MongoDB :", e)
            raise

    def get_database(self):
        """Retourne l'objet base de données."""
        if self.db is None:
            self.connect()
        return self.db
