import json
import re
import hashlib
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from jose import jwt
from pydantic import BaseModel
from fastapi.security.api_key import APIKeyHeader

SECRET_KEY = "MY_SECRET_KEY"
ALGORITHM = "HS256"
USER_FILE = "users.json"
app = FastAPI()
original_openapi = app.openapi



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = original_openapi()  

    openapi_schema["components"]["securitySchemes"] = {
        "Authorization": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"Authorization": []}]

    app.openapi_schema = openapi_schema
    return openapi_schema


app.openapi = custom_openapi
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)



class SignupModel(BaseModel):
    username: str
    password: str
    fname: str
    lname: str


class SigninModel(BaseModel):
    username: str
    password: str


def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open(USER_FILE, "w") as f:
            json.dump({"users": []}, f)
        return {"users": []}


def save_users(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=4)


def validate_username(username):
    return bool(re.fullmatch(r"[a-z]{4,}", username))


def validate_password(password):
    return (
        len(password) >= 5 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password) and
        not re.search(r"[^A-Za-z0-9]", password)
    )


def validate_name(name):
    return bool(re.fullmatch(r"[A-Za-z]+", name))


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



@app.post("/signup")
async def signup(body: SignupModel):

    username = body.username
    password = body.password
    fname = body.fname
    lname = body.lname

    if not validate_username(username):
        return JSONResponse(
            status_code=400,
            content={"result": False, "error": "Invalid username format"}
        )

    if not validate_password(password):
        return JSONResponse(
            status_code=400,
            content={"result": False, "error": "Invalid password format"}
        )

    if not validate_name(fname):
        return JSONResponse(
            status_code=400,
            content={"result": False, "error": "Invalid first name format"}
        )

    if not validate_name(lname):
        return JSONResponse(
            status_code=400,
            content={"result": False, "error": "Invalid last name format"}
        )

    data = load_users()

    if any(u["username"] == username for u in data["users"]):
        return JSONResponse(
            status_code=400,
            content={"result": False, "error": "User already exists"}
        )


    data["users"].append({
        "username": username,
        "password": hash_password(password),
        "fname": fname,
        "lname": lname
    })

    save_users(data)

    return JSONResponse(
        status_code=201,
        content={"result": True, "message": "SignUp success. Please proceed to Signin"}
    )


@app.post("/signin")
async def signin(body: SigninModel):

    username = body.username
    password = body.password

    data = load_users()
    hashed_pw = hash_password(password)

    for user in data["users"]:
        if user["username"] == username and user["password"] == hashed_pw:
            token = jwt.encode(
                {"username": username, "fname": user["fname"]},
                SECRET_KEY,
                algorithm=ALGORITHM
            )

            return {
                "result": True,
                "jwt": token,
                "message": "Signin success"
            }

    return JSONResponse(
        status_code=400,
        content={"result": False, "error": "Invalid Credentials"}
    )



@app.get("/user/me")
async def user_me(Authorization: str = Header(None)):
    if not Authorization:
        return JSONResponse(
            status_code=400,
            content={"result": False, "error": "Please provide a JWT token"}
        )

    
    token = Authorization.split(" ")[1] if Authorization.startswith("Bearer ") else Authorization

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"result": False, "error": "JWT Verification Failed"}
        )

    data = load_users()
    for user in data["users"]:
        if user["username"] == username:
            return {
                "result": True,
                "data": {
                    "fname": user["fname"],
                    "lname": user["lname"],
                    "password": user["password"]
                }
            }

    return JSONResponse(
        status_code=400,
        content={"result": False, "error": "User Not Found"}
    )
