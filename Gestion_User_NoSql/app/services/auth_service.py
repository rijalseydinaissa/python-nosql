import bcrypt
from db.mongodb import mongodb
from db.redis_sessions import redis_sessions
from models.user import User

class AuthService:
    def __init__(self):
        self.collection = mongodb.get_collection("users")

    def inscrire_utilisateur(self, nom, email, password, role):
        # Vérification si l'email est déjà utilisé
        if self.collection.find_one({"email": email}):
            print("Erreur : Cet email est déjà utilisé.")
            return
        
        # Vérification du rôle
        if role not in ["admin", "enseignant", "etudiant"]:
            print("Erreur : Rôle invalide.")
            return
        
        # Hachage du mot de passe avec bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Création d'un objet utilisateur et insertion dans la base de données
        user = User(nom, email, hashed_password, role)
        self.collection.insert_one(user.to_dict())
        print("Utilisateur inscrit avec succès.")

    def connexion(self, email, password):
        # Recherche de l'utilisateur par email
        user = self.collection.find_one({"email": email})
        if not user:
            print("Erreur : Utilisateur introuvable.")
            return None

        # Comparaison du mot de passe entré avec celui haché stocké dans la base de données
        # if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        #     print("Erreur : Mot de passe incorrect.")
        #     return None

        # Création d'un token de session
        session_token = redis_sessions.create_session(user["email"], user["role"])
        print(f"Connexion réussie ! Token de session : {session_token}")
        return session_token

    def verifier_session(self, token):
        return redis_sessions.get_session(token)

    def deconnexion(self, token):
        redis_sessions.delete_session(token)
        print("Déconnexion réussie.")

# Instance de AuthService
auth_service = AuthService()
