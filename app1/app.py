from fastapi import FastAPI, HTTPException
import redis
import os

app = FastAPI()

# Read Redis connection settings from environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT_RAW = os.getenv("REDIS_PORT", "6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")  # can be None

# Safety: handle possible bad REDIS_PORT format
try:
    REDIS_PORT = int(REDIS_PORT_RAW)
except ValueError:
    # If Kubernetes injected a weird tcp:// format → extract port number
    import re
    match = re.search(r':(\d+)', REDIS_PORT_RAW)
    REDIS_PORT = int(match.group(1)) if match else 6379

# Connect to Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

@app.get("/")
def root():
    return {"message": "FastAPI is working"}

@app.post("/cache")
def store_value(key: str, value: str):
    r.set(key, value)
    return {"message": f"Stored key '{key}'"}

@app.get("/cache")
def get_value(key: str):
    value = r.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value.decode()}

@app.get("/secret-test")
def show_secret():
    return {"password": os.getenv("REDIS_PASSWORD")}
