class Etudiant:
    def __init__(self, nom, prenom, email,telephone, classe, notes):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone
        self.classe = classe
        self.notes = notes

    def moyenne(self):
        return sum(self.notes) / len(self.notes) if self.notes else 0

    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "telephone": self.telephone,
            "classe": self.classe,
            "notes": self.notes,
            "moyenne": self.moyenne()
        }
