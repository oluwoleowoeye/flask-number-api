from flask import Flask, request, jsonify
from flask_cors import CORS
import math
from flask_compress import Compress  # For GZIP compression
import logging

app = Flask(__name__)
CORS(app)
Compress(app)  # Enable response compression

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def is_armstrong(number):
    """Check if a number is an Armstrong (Narcissistic) number."""
    try:
        num_str = str(abs(int(number)))  # Convert to string, ignore negative sign
        power = len(num_str)
        return sum(int(d) ** power for d in num_str) == abs(number)
    except Exception as e:
        logger.error(f"Error in is_armstrong: {e}")
        return False

def is_prime(number):
    """Check if a number is prime (optimized 6k ± 1 method)."""
    try:
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
    except Exception as e:
        logger.error(f"Error in is_prime: {e}")
        return False

def is_perfect(number):
    """Check if a number is a perfect number (sum of divisors equals the number)."""
    try:
        if number < 1:
            return False
        return sum(i for i in range(1, number) if number % i == 0) == number
    except Exception as e:
        logger.error(f"Error in is_perfect: {e}")
        return False

def get_digit_sum(number):
    """Calculate the sum of digits of a number."""
    try:
        return sum(int(digit) for digit in str(abs(int(number))))  # Ignore decimals and negative sign
    except Exception as e:
        logger.error(f"Error in get_digit_sum: {e}")
        return 0

@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    """Classify a given number quickly."""
    number_str = request.args.get("number", "").strip()

    # Check if the input is a valid number (integer or float)
    try:
        number = float(number_str)  # Convert input to float
        if number.is_integer():  
            number = int(number)  # Convert to integer if no decimal part
    except ValueError:
        # Return 400 Bad Request with the required JSON response format
        return jsonify({"number": number_str, "error": True}), 400  

    try:
        # Calculate properties
        properties = []
        if is_armstrong(number):
            properties.append("armstrong")
        properties.append("even" if number % 2 == 0 else "odd")

        response_data = {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": get_digit_sum(number),
            "fun_fact": f"{number} is an Armstrong number because ..." if "armstrong" in properties else None
        }

        return jsonify(response_data), 200  # Always return 200 for valid numbers

    except Exception as e:
        logger.error(f"Error in classify_number endpoint: {e}")
        return jsonify({"error": "Internal server error, please try again later."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)  # Enable multi-threading
