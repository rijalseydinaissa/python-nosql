import json
import pandas as pd
from pymongo import errors


class EtudiantService:
    def __init__(self, mongo_client, redis_cache):
        self.mongo_client = mongo_client
        self.redis_cache = redis_cache
        self.db = self.mongo_client.get_database()
        self.etudiants_collection = self.db["etudiants"]

    @staticmethod
    def validate_notes(notes):
        """Vérifie que toutes les notes sont comprises entre 0 et 20."""
        return all(0 <= note <= 20 for note in notes)

    def ajouter_etudiant(self, nom, prenom, telephone, classe, notes):
        """Ajoute un étudiant en base de données et dans le cache Redis."""
        if not self.validate_notes(notes):
            print("Erreur : une ou plusieurs notes ne sont pas comprises entre 0 et 20.")
            return

        # Vérification de l'unicité du téléphone
        if self.etudiants_collection.find_one({"telephone": telephone}):
            print("Erreur : un étudiant avec ce numéro de téléphone existe déjà.")
            return

        etudiant = {
            "nom": nom,
            "prenom": prenom,
            "telephone": telephone,
            "classe": classe,
            "notes": notes
        }

        try:
            insertion_result = self.etudiants_collection.insert_one(etudiant)
            print("Étudiant ajouté dans MongoDB avec l'ID :", insertion_result.inserted_id)
        except errors.PyMongoError as e:
            print("Erreur lors de l'insertion dans MongoDB :", e)
            return

        # Mise en cache dans Redis
        self.redis_cache.cache_student(telephone, etudiant)

    def recuperer_etudiant(self):
        """Récupère les étudiants depuis Redis ou MongoDB."""
        etudiants = []
        redis_client = self.redis_cache.get_client()

        keys = redis_client.keys("etudiant*")
        if keys:
            for key in keys:
                valeur = redis_client.get(key)
                if valeur:
                    etudiant = json.loads(valeur)
                    etudiants.append(etudiant)
            print("Étudiants récupérés depuis Redis")
        else:
            etudiants = list(self.etudiants_collection.find())
            print("Étudiants récupérés depuis MongoDB")
        
        return etudiants

    @staticmethod
    def afficher_etudiant(etudiants):
        """Affiche les étudiants sous forme de tableau."""
        if etudiants:
            df = pd.DataFrame(etudiants)
            print(df)
        else:
            print("Aucun étudiant à afficher")