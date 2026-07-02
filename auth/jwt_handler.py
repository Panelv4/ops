import jwt
import datetime

SECRET = "supersecretkey"

def generate_token(user):
    payload = {
        "user_id": user["id"],
        "company_id": user["company_id"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        return None
