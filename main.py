from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import math
from flask_compress import Compress  # For GZIP compression

app = Flask(__name__)
CORS(app)
Compress(app)  # Enable response compression

def is_armstrong(number):
    """Check if a number is an Armstrong (Narcissistic) number."""
    digits = list(map(int, str(number)))
    power = len(digits)
    return sum(d ** power for d in digits) == number

def is_prime(number):
    """Check if a number is prime (optimized 6k ± 1 method)."""
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
    """Check if a number is a perfect number (sum of divisors equals the number)."""
    if number < 2:
        return False
    return sum(i for i in range(1, number) if number % i == 0) == number

def get_digit_sum(number):
    """Calculate the sum of digits of a number."""
    return sum(int(digit) for digit in str(number))

@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    """Classify a number and return the required JSON format."""
    number = request.args.get("number", "").strip()

    if not number.isdigit():
        return jsonify({
            "number": number,
            "error": True
        }), 400  # Bad request for invalid input

    number = int(number)

    # Determine Armstrong status
    is_armstrong_num = is_armstrong(number)
    
    # Determine even/odd status
    is_even = number % 2 == 0

    # Build properties list
    if is_armstrong_num and is_even:
        properties = ["armstrong", "even"]
    elif is_armstrong_num and not is_even:
        properties = ["armstrong", "odd"]
    elif not is_armstrong_num and is_even:
        properties = ["even"]
    else:
        properties = ["odd"]

    digit_sum = get_digit_sum(number)
    fun_fact = f"{number} is {'an Armstrong' if is_armstrong_num else 'not an Armstrong'} number."

    response_data = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

    return jsonify(response_data), 200  # Return a successful response

if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)  # Enable multi-threading
