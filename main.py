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

def is_perfect(number):
    """Check if a number is a perfect number (sum of its proper divisors equals the number)."""
    if number < 2:
        return False
    divisors = [1] + [i for i in range(2, number // 2 + 1) if number % i == 0]
    return sum(divisors) == number

def get_digit_sum(number):
    """Calculate sum of the digits of a number."""
    return sum(map(int, str(number)))

def get_fun_fact(number):
    """Fetch number trivia with a timeout for speed."""
    try:
        response = requests.get(f"http://numbersapi.com/{number}/math", timeout=0.4)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return "No fun fact available at the moment."

@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    """Classify a given number and return its properties."""
    number = request.args.get("number", "").strip()

    if not number.isdigit():
        return jsonify({
            "number": number,
            "error": True
        }), 400
    
    number = int(number)

    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    if is_prime(number):
        properties.append("prime")
    if is_perfect(number):
        properties.append("perfect")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    response_data = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": get_digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response_data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)  # Enable multi-threading
