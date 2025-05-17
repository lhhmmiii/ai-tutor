from redis import Redis
import os

redis_host = os.getenv("REDIS_HOST", "localhost")

redis_client = Redis(
    host=redis_host,
    port=6379,
    db=0,
    decode_responses=True  # Trả string thay vì bytes
)

