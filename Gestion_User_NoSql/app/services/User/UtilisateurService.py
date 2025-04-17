import hashlib

class UtilisateurService:
    def __init__(self):
        # Simule une base de données des utilisateurs avec leur rôle
        self.utilisateurs = {
            "admin": {"mot_de_passe": self._hash_password("admin123"), "role": "admin"},
            "user": {"mot_de_passe": self._hash_password("user123"), "role": "utilisateur"},
        }
        self.utilisateur_actuel = None  # Stocke l'utilisateur connecté

    def _hash_password(self, mot_de_passe):
        """Hache le mot de passe pour éviter de stocker en clair."""
        return hashlib.sha256(mot_de_passe.encode()).hexdigest()

    def connexion(self, identifiant, mot_de_passe):
        """Vérifie les identifiants et connecte l'utilisateur."""
        utilisateur = self.utilisateurs.get(identifiant)
        if utilisateur and utilisateur["mot_de_passe"] == self._hash_password(mot_de_passe):
            self.utilisateur_actuel = {"identifiant": identifiant, "role": utilisateur["role"]}
            print(f"Connexion réussie ! Bienvenue, {identifiant}.")
            return True
        else:
            print("Identifiant ou mot de passe incorrect.")
            return False

    def est_admin(self):
        """Vérifie si l'utilisateur actuel est un admin."""
        return self.utilisateur_actuel and self.utilisateur_actuel["role"] == "admin"
