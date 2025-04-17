import bcrypt

class User:
    def __init__(self, nom, email, password, role):
        self.nom = nom
        self.email = email
        self.password = self.hash_password(password)
        self.role = role  # 'admin', 'enseignant', 'etudiant'

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password.encode())

    def to_dict(self):
        return {
            "nom": self.nom,
            "email": self.email,
            "password": self.password,
            "role": self.role
        }
