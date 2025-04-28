import os
import logging
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, request, jsonify, Response, stream_with_context
from jose import jwt, JWTError
from flask_cors import CORS
from groq import Groq
from jwt_utils import verify_token

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)
SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

app = Flask(__name__)
CORS(app)  # Allow requests from Next.js frontend

@app.route("/protected", methods=["GET"])
def protected():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    user = verify_token(token)

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"message": "Hello from Flask!", "user": user})

@app.route('/chat', methods=["POST"])
def stream():
    def generate():
        data = request.get_json()
        query = data.get("query", "")
        logging.info(f"Query received: {query}")

        if not query:
            return jsonify({"error": "Missing 'query' in request body"}), 400

        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": query}
            ],
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\n\n"
        yield "data: [DONE]\n\n"

    return Response(stream_with_context(generate()), content_type='text/event-stream')

# Run the server
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)