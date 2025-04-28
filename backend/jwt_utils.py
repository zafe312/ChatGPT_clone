import os
import logging
from dotenv import load_dotenv
from pathlib import Path
from jose import jwt, JWTError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)
SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET")

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