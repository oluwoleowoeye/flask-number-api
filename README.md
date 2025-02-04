Flask Number Classification API

A simple Flask API that classifies numbers based on their mathematical properties such as prime, perfect, Armstrong, even/odd, and digit sum.

🚀 Features

Classifies numbers as Armstrong, Prime, Perfect, Even/Odd.

Returns digit sum and fun facts about the number.

Supports CORS and GZIP compression for fast API responses.

Handles invalid inputs gracefully with appropriate error messages.

📦 Installation

1️⃣ Clone the Repository

git clone https://github.com/oluwoleowoeye/flask-number-api.git

cd flask-number-api

2️⃣ Create a Virtual Environment & Install Dependencies

python3 -m venv venv

source venv/bin/activate # On Linux/macOS

pip install -r requirements.txt

3️⃣ Run the Application Locally

gunicorn --bind 0.0.0.0:5000 main:app

🔥 API Usage

📌 Endpoint:

GET /api/classify-number?number=

Example:

http://your-ec2-public-ip:5000/api/classify-number?number=371

✅ Example Response (200 OK)

{ "number": 371, "is_prime": false, "is_perfect": false, "properties": ["armstrong", "odd"], "digit_sum": 11, "fun_fact": "371 is an Armstrong number." }

❌ Error Response (400 Bad Request)

{ "number": "alphabet", "error": true }

🔗 Deployment on AWS EC2

1️⃣ Connect to EC2 Instance

ssh -i your-key.pem ubuntu@your-ec2-public-ip

2️⃣ Pull Latest Code & Restart Gunicorn

cd ~/flask-number-api

git pull origin main

source venv/bin/activate

pip install -r requirements.txt

sudo systemctl restart gunicorn

3️⃣ Test the API

Go to your browser and enter the address below in your search bar:

http://your-ec2-public-ip:5000/api/classify-number?number=371

🛠 Tech Stack

Flask (Python backend)

Gunicorn (WSGI server)

AWS EC2 (Deployment)

👨‍💻 Author

Oluwole Owoeye

📧 Email: wolexcharles@yahoo.com

🔗 GitHub: https://github.com/oluwoleowoeye
