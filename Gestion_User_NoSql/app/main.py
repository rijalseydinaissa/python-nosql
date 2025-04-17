from services.auth_service import auth_service
from services.etudiant_service import service_etudiant
from models.etudiant import Etudiant

session_token = None

def menu_auth():
    """Menu d'authentification : Inscription, Connexion, Quitter"""
    global session_token
    while True:
        print("\n1. Inscription")
        print("2. Connexion")
        print("3. Quitter")

        choix = input("Votre choix : ").strip()
        
        if choix == "1":
            nom = input("Nom : ").strip()
            email = input("Email : ").strip()
            password = input("Mot de passe : ").strip()
            role = input("Rôle (admin/enseignant/etudiant) : ").strip().lower()
            if role not in ["admin", "enseignant", "etudiant"]:
                print("Rôle invalide. Veuillez choisir entre admin, enseignant ou etudiant.")
                continue
            auth_service.inscrire_utilisateur(nom, email, password, role)

        elif choix == "2":
            email = input("Email : ").strip()
            password = input("Mot de passe : ").strip()
            session_token = auth_service.connexion(email, password)
            if session_token:
                menu_principal()

        elif choix == "3":
            break

        else:
            print("Choix invalide. Veuillez réessayer.")

def menu_principal():
    """Menu principal selon le rôle de l'utilisateur connecté"""
    global session_token
    session_data = auth_service.verifier_session(session_token)
    if not session_data:
        print("Session invalide. Veuillez vous reconnecter.")
        return menu_auth()

    role = session_data["role"]
    print(f"\nBienvenue {session_data['email']} ({role})")

    while True:
        if role == "admin":
            print("\n1. Ajouter un étudiant")
            print("2. Afficher les étudiants")
            print("3. Modifier les notes")
            print("5. Déconnexion")

        elif role == "enseignant":
            print("\n1. Calculer la moyenne d'une classe")
            print("2. Exporter en CSV")
            print("3. Générer un rapport PDF")
            print("4. Envoyer une notification")
            print("5. Déconnexion")

        elif role == "etudiant":
            print("\n1. Voir mes notes")
            print("5. Déconnexion")

        choix = input("Votre choix : ").strip()

        # 🟢 Actions Admin
        if choix == "1" and role == "admin":
            nom = input("Nom : ").strip()
            prenom = input("Prénom : ").strip()
            email = input("Email : ").strip()
            telephone = input("Téléphone : ").strip()
            classe = input("Classe : ").strip()
            notes = list(map(int, input("Notes (séparées par des espaces) : ").split()))
            etudiant = Etudiant(nom, prenom,email, telephone, classe, notes)
            service_etudiant.ajouter_etudiant(etudiant)

        elif choix == "2" and role == "admin":
            etudiants = service_etudiant.recuperer_etudiants()
            for e in etudiants:
                print(e)

        elif choix == "3" and role == "admin":
            telephone = input("Téléphone de l'étudiant : ").strip()
            notes = list(map(int, input("Nouvelles notes : ").split()))
            service_etudiant.modifier_notes(telephone, notes)

        # 🟡 Actions Enseignant
        elif choix == "1" and role == "enseignant":
            classe = input("Nom de la classe : ").strip()
            moyenne = service_etudiant.calculer_moyenne_generale(classe)
            if moyenne is not None:
                print(f"La moyenne de la classe {classe} est de {moyenne:.2f}")
            else:
                print("Aucun étudiant trouvé pour cette classe.")

        elif choix == "2" and role == "enseignant":
            service_etudiant.exporter_csv()
        
        elif choix == "3" and role == "enseignant":
            service_etudiant.generer_rapport_pdf()
        
        elif choix == "4" and role == "enseignant":
            message = input("Message à envoyer : ").strip()
            email = input("Email de l'étudiant : ").strip()
            service_etudiant.envoyer_notification(email, message)

        # 🔵 Action Étudiant
        elif choix == "1" and role == "etudiant":
            etudiant = service_etudiant.recuperer_etudiant_par_email(session_data["email"])
            if etudiant:
                print(f"Notes de {etudiant.nom} {etudiant.prenom} : {etudiant.notes}")
            else:
                print("Aucune donnée trouvée.")

        # 🚪 Déconnexion
        elif choix == "5":
            auth_service.deconnexion(session_token)
            return menu_auth()

        else:
            print("Action non autorisée ou choix invalide.")

if __name__ == "__main__":
    menu_auth()
