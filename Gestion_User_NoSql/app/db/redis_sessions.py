import redis
import uuid

class RedisSessions:
    def __init__(self):
        self.client = redis.Redis(host="localhost", port=6379, decode_responses=True)

    def create_session(self, email, role):
        token = str(uuid.uuid4())
        self.client.setex(f"session:{token}", 3600, f"{email},{role}")
        return token

    def get_session(self, token):
        session = self.client.get(f"session:{token}")
        if session:
            email, role = session.split(",")
            return {"email": email, "role": role}
        return None

    def delete_session(self, token):
        self.client.delete(f"session:{token}")

redis_sessions = RedisSessions()
