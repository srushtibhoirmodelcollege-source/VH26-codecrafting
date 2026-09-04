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