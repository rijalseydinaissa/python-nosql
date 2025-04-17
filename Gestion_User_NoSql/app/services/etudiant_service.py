from db.mongodb import mongodb
from db.redis_cache import redis_cache
from services.NotificationService import NotificationService
from services.SmsService import SmsService
from models.etudiant import Etudiant
import csv
import smtplib
from fpdf import FPDF
import os
class EtudiantService:
    def __init__(self):
        self.collection = mongodb.get_collection("etudiants")

    def ajouter_etudiant(self, etudiant):
        if self.collection.find_one({"telephone": etudiant.telephone}):
            print("Erreur : Un étudiant avec ce téléphone existe déjà.")
            return

        if not all(0 <= note <= 20 for note in etudiant.notes):
            print("Erreur : Les notes doivent être entre 0 et 20.")
            return

        etudiant_dict = etudiant.to_dict()
        etudiant_dict["moyenne"] = sum(etudiant.notes) / len(etudiant.notes) if etudiant.notes else 0
        self.collection.insert_one(etudiant_dict)
        etudiant_dict["_id"] = str(etudiant_dict["_id"])
        redis_cache.set_cache(f"etudiant:{etudiant.telephone}", etudiant_dict)
        print("Étudiant ajouté avec succès.")

    def recuperer_etudiants(self):
        etudiants = [redis_cache.get_cache(key) for key in redis_cache.client.keys("etudiant:*")]
        if not etudiants:
            etudiants = list(self.collection.find())
        return etudiants

    def rechercher_etudiant(self, critere, valeur):
        return self.collection.find_one({critere: valeur})

    def calculer_moyenne_generale(self, classe):
        etudiants = self.collection.find({"classe": classe})
        notes = [sum(etudiant["notes"]) / len(etudiant["notes"]) for etudiant in etudiants if etudiant["notes"]]
        return sum(notes) / len(notes) if notes else 0

    def trier_etudiants_par_moyenne(self):
        return sorted(self.recuperer_etudiants(), key=lambda e: e["moyenne"], reverse=True)[:10]

    def modifier_notes(self, telephone, nouvelles_notes):
        if not all(0 <= note <= 20 for note in nouvelles_notes):
            print("Erreur : Notes invalides.")
            return

        moyenne = sum(nouvelles_notes) / len(nouvelles_notes) if nouvelles_notes else 0
        self.collection.update_one(
            {"telephone": telephone}, 
            {"$set": {"notes": nouvelles_notes, "moyenne": moyenne}}
        )
        etudiant = self.rechercher_etudiant("telephone", telephone)
        if etudiant:
            redis_cache.set_cache(f"etudiant:{telephone}", etudiant)
            print("Notes mises à jour.")
            self.envoyer_notification(etudiant["email"], "Vos notes ont été mises à jour.")
            if moyenne < 10:
                self.envoyer_notification(etudiant["email"], "⚠️ Alerte : Votre moyenne est en dessous de 10/20.")

    def supprimer_etudiant(self, telephone):
        self.collection.delete_one({"telephone": telephone})
        redis_cache.delete_cache(f"etudiant:{telephone}")
        print("Étudiant supprimé.")
    
    def exporter_csv(self, nom_fichier="etudiants.csv"):
        etudiants = self.recuperer_etudiants()

        if not etudiants:
            print("Aucun étudiant à exporter.")
            return

        try:
            with open(nom_fichier, mode="w", newline="", encoding="utf-8") as fichier_csv:
                champs = ["nom", "prenom", "telephone", "classe", "notes", "moyenne"]
                writer = csv.DictWriter(fichier_csv, fieldnames=champs)
                
                writer.writeheader()
                for etudiant in etudiants:
                    writer.writerow({
                        "nom": etudiant["nom"],
                        "prenom": etudiant["prenom"],
                        "telephone": etudiant["telephone"],
                        "classe": etudiant["classe"],
                        "notes": ", ".join(map(str, etudiant["notes"])),
                        # "moyenne": etudiant["moyenne"]
                    })

            print(f"✅ Exportation réussie : {nom_fichier}")
        except Exception as e:
            print("❌ Erreur lors de l'exportation CSV :", e)

    def generer_rapport_pdf(self, nom_fichier="rapport_etudiants.pdf"):
        etudiants = self.recuperer_etudiants()
        if not etudiants:
            print("Aucun étudiant à inclure dans le rapport.")
            return
        
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Rapport des étudiants", ln=True, align="C")

        pdf.set_font("Arial", size=12)
        for etudiant in etudiants:
            pdf.cell(0, 10, f"{etudiant['nom']} {etudiant['prenom']} - {etudiant['classe']}", ln=True)
            pdf.cell(0, 10, f"Notes: {', '.join(map(str, etudiant['notes']))}", ln=True)
            pdf.ln(5)

        pdf.output(nom_fichier)
        print(f"✅ Rapport PDF généré : {nom_fichier}")


    def envoyer_notification(self, email, message):
        try:
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_user = "sididiop53@gmail.com"
            smtp_password = "mzfiinfxftbaafki" 
            
            if not smtp_password:
                raise ValueError("Le mot de passe SMTP est manquant. Vérifiez vos variables d'environnement.")

            email = email.strip()

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                msg = f"From: {smtp_user}\r\nTo: {email}\r\nSubject: Notification\r\n\r\n{message}"
                server.sendmail(smtp_user, email, msg)

            print(f"✅ Notification envoyée à {email}")
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de la notification : {e}")





    # def alerter_moyenne_basse(self, telephone, email):
    #     etudiant = self.rechercher_etudiant("telephone", telephone)
    #     if etudiant:
    #         moyenne = sum(etudiant["notes"]) / len(etudiant["notes"])
    #         if moyenne < 10:
    #             message = f"⚠️ Alerte : Votre moyenne est inférieure à 10/20 !"
    #             # Envoi de l'alerte par SMS ou par e-mail
    #             SmsService.envoyer_sms(telephone, message)
    #             NotificationService.envoyer_email(email, "Alerte Moyenne Basse", message)


# Instance du service
service_etudiant = EtudiantService()
