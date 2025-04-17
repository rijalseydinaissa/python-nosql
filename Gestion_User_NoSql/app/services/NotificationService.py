import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class NotificationService:
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def envoyer_email(self, destinataire, sujet, message):
        msg = MIMEMultipart()
        msg["From"] = self.smtp_user
        msg["To"] = destinataire
        msg["Subject"] = sujet

        msg.attach(MIMEText(message, "plain"))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                text = msg.as_string()
                server.sendmail(self.smtp_user, destinataire, text)
                print("E-mail envoyé avec succès.")
        except Exception as e:
            print(f"Erreur d'envoi d'e-mail: {e}")

# Exemple d'utilisation :
# notification_service = NotificationService("smtp.gmail.com", 587, "ton_email@gmail.com", "ton_mot_de_passe")
# notification_service.envoyer_email("destinataire@example.com", "Nouvelle Note Ajoutée", "Votre nouvelle note a été ajoutée.")
