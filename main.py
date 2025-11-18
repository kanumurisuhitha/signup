import json
import re
import hashlib
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from typing import Optional
from jose import jwt
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"result": False, "message": "fields can't be empty"},
    )

app = FastAPI()

USER_DB = "users.json"
SECRET_KEY = "IGNOSIS_SECRET_KEY"
ALGORITHM = "HS256"


# -------------------------
# Helper Functions
# -------------------------
def load_users():
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except:
        return []


def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def validate_username(username):
    return bool(re.fullmatch(r"[a-z]{4,}", username))


def validate_password(password):
    if len(password) < 5:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if re.search(r"[^A-Za-z0-9]", password):
        return False
    return True


def validate_name(name):
    return bool(re.fullmatch(r"[A-Za-z]+", name))


# -------------------------
# Routes
# -------------------------

@app.post("/signup")
def signup(body: dict):
    required = ["username", "password", "fname", "lname"]
    if not body or any(k not in body for k in required):
        raise HTTPException(status_code=400, detail="Invalid body")

    username = body["username"]
    password = body["password"]
    fname = body["fname"]
    lname = body["lname"]

    # Validations
    if not validate_username(username):
        raise HTTPException(status_code=400, detail="Invalid username")

    if not validate_password(password):
        raise HTTPException(status_code=400, detail="Invalid password")

    if not validate_name(fname) or not validate_name(lname):
        raise HTTPException(status_code=400, detail="Invalid name fields")

    users = load_users()

    # Check if exists
    if any(u["username"] == username for u in users):
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(password)

    new_user = {
        "username": username,
        "password": hashed,
        "fname": fname,
        "lname": lname
    }

    users.append(new_user)
    save_users(users)

    return JSONResponse(
        status_code=201,
        content={
            "result": True,
            "message": "SignUp success. Please proceed to Signin"
        }
    )


@app.post("/signin")
def signin(body: dict):
    if not body or "username" not in body or "password" not in body:
        raise HTTPException(status_code=400, detail="Invalid body")

    username = body["username"]
    password = body["password"]
    hashed = hash_password(password)

    users = load_users()

    user = next((u for u in users if u["username"] == username and u["password"] == hashed), None)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    payload = {
        "username": user["username"],
        "fname": user["fname"],
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "result": True,
        "jwt": token,
        "message": "Signin success"
    }


@app.get("/user/me")
def get_me(authorization: Optional[str] = Header(None)):
    if not authorization:
        return JSONResponse(
            status_code=400,
            content={
                "result": False,
                "error": "Please provide a JWT token"
            }
        )

    try:
        data = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return JSONResponse(
            status_code=400,
            content={
                "result": False,
                "error": "JWT Verification Failed"
            }
        )

    users = load_users()
    user = next((u for u in users if u["username"] == data["username"]), None)

    return {
        "result": True,
        "data": {
            "fname": user["fname"],
            "lname": user["lname"],
            "password": user["password"]
        }
    }
