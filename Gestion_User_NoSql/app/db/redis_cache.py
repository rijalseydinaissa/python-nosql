import redis
import json

class RedisCache:
    def __init__(self):
        try:
            self.client = redis.Redis(host="localhost", port=6379, decode_responses=True)
            self.client.ping()  # Vérifier la connexion
        except redis.ConnectionError as e:
            print("Erreur de connexion à Redis :", e)
            raise

    def set_cache(self, key, value):
        self.client.set(key, json.dumps(value))

    def get_cache(self, key):
        value = self.client.get(key)
        return json.loads(value) if value else None

    def delete_cache(self, key):
        self.client.delete(key)

redis_cache = RedisCache()
