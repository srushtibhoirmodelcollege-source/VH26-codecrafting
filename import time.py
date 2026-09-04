import time


def calculate_score(frequency, recency, retrieval_cost, latency, popularity, size_efficiency):
    score = (
        0.30 * frequency
        + 0.20 * recency
        + 0.20 * retrieval_cost
        + 0.10 * latency
        + 0.10 * popularity
        + 0.10 * size_efficiency
    )

    return round(score, 2)


def check_stale(last_updated, ttl):
    current_time = time.time()

    if current_time - last_updated > ttl:
        return True
    else:
        return False


def decide_action(score, is_stale=False):
    if is_stale:
        return "REFRESH"

    if score >= 80:
        return "RETAIN"
    elif score >= 50:
        return "MONITOR"
    else:
        return "EVICT"


def get_reason(data, action):
    reasons = []

    if data["frequency"] < 40:
        reasons.append("Low access frequency")

    if data["recency"] < 40:
        reasons.append("Not recently accessed")

    if data["retrieval_cost"] > 70:
        reasons.append("Expensive to retrieve")

    if data["size_efficiency"] < 40:
        reasons.append("Large memory footprint")

    if data["popularity"] < 40:
        reasons.append("Low popularity")

    if action == "REFRESH":
        reasons.append("Data is stale")

    if not reasons:
        reasons.append("Good overall value")

    return reasons


# Test objects

objects = [
    {
        "name": "product_1",
        "frequency": 90,
        "recency": 85,
        "retrieval_cost": 95,
        "latency": 80,
        "popularity": 90,
        "size_efficiency": 90
    },
    {
        "name": "old_image",
        "frequency": 20,
        "recency": 15,
        "retrieval_cost": 30,
        "latency": 20,
        "popularity": 10,
        "size_efficiency": 20
    },
    {
        "name": "user_profile",
        "frequency": 65,
        "recency": 70,
        "retrieval_cost": 80,
        "latency": 75,
        "popularity": 60,
        "size_efficiency": 85
    }
]


for obj in objects:
    score = calculate_score(
        obj["frequency"],
        obj["recency"],
        obj["retrieval_cost"],
        obj["latency"],
        obj["popularity"],
        obj["size_efficiency"]
    )

    action = decide_action(score)

    print("--------------------")
    print("Object:", obj["name"])
    print("Score:", score)
    print("Decision:", action)

    reasons = get_reason(obj, action)

    print("Reasons:")
    for reason in reasons:
        print("-", reason)


# Automatic stale test

print("\n--- REFRESH TEST ---")

last_updated = time.time() - 120
ttl = 60

is_stale = check_stale(last_updated, ttl)

score = 85
action = decide_action(score, is_stale)

print("Data stale:", is_stale)
print("Score:", score)
print("Decision:", action)


import fastapi
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = {}
@app.post("/cache/add/{key}/{value}")
def add_cache(key: str, value: str):
    cache[key] = value
    return {
        "message": "Data added",
        "key": key,
        "value": value
    }


@app.get("/cache/get/{key}")
def get_cache(key: str):
    if key in cache:
        return {
            "found": True,
            "key": key,
            "value": cache[key]
        }

    return {
        "found": False,
        "message": "Key not found"
    }


@app.delete("/cache/evict/{key}")
def evict_cache(key: str):
    if key in cache:
        del cache[key]
        return {
            "message": "Data evicted",
            "key": key
        }

    return {
        "message": "Key not found"
    }


@app.get("/cache/status")
def cache_status():
    return {
        "size": len(cache),
        "data": cache
    }