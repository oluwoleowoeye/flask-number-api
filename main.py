from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import math
from flask_compress import Compress  # For GZIP compression

app = Flask(__name__)
CORS(app)
Compress(app)  # Enable response compression

def is_armstrong(number):
    """Efficient Armstrong (Narcissistic) number check."""
    digits = list(map(int, str(number)))
    power = len(digits)
    return sum(d ** power for d in digits) == number

def is_prime(number):
    """Optimized prime check using 6k ± 1 optimization."""
    if number < 2:
        return False
    if number in (2, 3):
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(number)) + 1, 6):
        if number % i == 0 or number % (i + 2) == 0:
            return False
    return True

@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    """Classify a given number quickly."""
    number = request.args.get("number", "").strip()
    
    if not number.isdigit():
        return jsonify({"error": "Invalid input. Please provide a valid integer."}), 400
    
    number = int(number)

    response_data = {
        "number": number,
        "classifications": {
            "is_armstrong": is_armstrong(number),
            "is_prime": is_prime(number),
            "is_even": number % 2 == 0
        }
    }

    return jsonify(response_data), 200

@app.route("/api/number-fact", methods=["GET"])
def number_fact():
    """Fetch number trivia with a timeout for speed."""
    number = request.args.get("number", "").strip()

    if not number.isdigit():
        return jsonify({"error": "Invalid input. Please provide a valid integer."}), 400
    
    try:
        response = requests.get(f"http://numbersapi.com/{number}/math", timeout=0.4)  # Set timeout to 400ms
        response.raise_for_status()
        fact = response.text
    except requests.RequestException:
        return jsonify({"error": "Failed to fetch number fact"}), 400  # Treat failures as 400

    return jsonify({"number": number, "fact": fact}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)  # Enable multi-threading

