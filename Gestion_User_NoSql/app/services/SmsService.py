from twilio.rest import Client

class SmsService:
    def __init__(self, account_sid, auth_token):
        self.client = Client(account_sid, auth_token)

    def envoyer_sms(self, numero_destinataire, message):
        message = self.client.messages.create(
            body=message,
            from_='+1234567890',  # Ton numéro Twilio
            to=numero_destinataire
        )
        print(f"SMS envoyé à {numero_destinataire}: {message.sid}")


