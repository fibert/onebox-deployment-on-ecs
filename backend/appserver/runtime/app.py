import json
import random
from collections import defaultdict

from flask import Flask
from flask import abort

# --- Init ---

app = Flask(__name__)

compliment_dict = {
    0: "You have a great sense of humor",
    1: "You're a good listener",
    2: "You have a beautiful smile",
    3: "You're very creative",
    4: "You're a hard worker",
    5: "You have a kind heart",
    6: "You always make others feel welcome",
    7: "You're very intelligent",
    8: "You have a great fashion sense",
    9: "You're an inspiration to others",
}

statistics_counters = defaultdict(int)

HEALTH_OK = "OK"

# --- API Functions ---


@app.route("/compliment/random")
def get_random_compliment() -> str:
    random_id, random_compliment = random.choice(list(compliment_dict.items()))
    increase_compliment_statistics_counter(random_id)
    return json.dumps({"compliment": random_compliment})


@app.route("/compliment/<int:compliment_id>")
def get_compliment_by_id(compliment_id: int) -> str:
    if not is_valid_compliment_id(compliment_id):
        abort(400)

    increase_compliment_statistics_counter(compliment_id)
    return json.dumps({"compliment": compliment_dict[compliment_id]})


@app.route("/statistics")
def get_all_counters() -> str:
    return json.dumps(get_all_compliment_statistics_counters())


@app.route("/statistics/<int:compliment_id>")
def get_counter_by_id(compliment_id: int) -> str:
    if not is_valid_compliment_id(compliment_id):
        abort(400)

    return json.dumps({"counter": get_compliment_statistics_counter(compliment_id)})


@app.route("/health")
def get_health() -> str:
    return json.dumps({"status": HEALTH_OK})


# --- Helper functions ---


def is_valid_compliment_id(compliment_id: int) -> bool:
    return 0 <= compliment_id < len(compliment_dict.keys())


def increase_compliment_statistics_counter(compliment_id: int) -> int:
    statistics_counters[compliment_id] += 1
    return statistics_counters[compliment_id]


def get_compliment_statistics_counter(compliment_id: int) -> int:
    return statistics_counters[compliment_id]


def get_all_compliment_statistics_counters() -> dict[int]:
    return dict(statistics_counters)


# --- Main ---

if __name__ == "__main__":
    app.run(host="0.0.0.0")
