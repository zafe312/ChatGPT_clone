import os
import logging
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, request, jsonify
from jose import jwt, JWTError
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)
SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET")

app = Flask(__name__)
CORS(app)  # Allow requests from Next.js frontend

def verify_token(token):
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False}  # 🔥 Ignore audience validation
        )
        return payload
    except JWTError as e:
        print("Token decode error:", e)
        return None

@app.route("/protected", methods=["GET"])
def protected():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user = verify_token(token)

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"message": "Hello from Flask!", "user": user})


# Run the server
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)