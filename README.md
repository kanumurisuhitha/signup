# 🚀 Authentication Desk — FastAPI Backend

This project is a complete authentication system built using **FastAPI** for the. It includes user signup, login, and authenticated user retrieval with strict validations and JWT-based authentication.

---

## 🔐 Signup API — `POST /signup`
- Validates empty body  
- Validates username format (alphanumeric only)  
- Validates password pattern  
- Prevents duplicate usernames  
- Hashes password using SHA-256  
- Returns response in the exact required format  

---

## 🔑 Login API — `POST /login`
- Validates username & password  
- Validates request signature header  
- Generates JWT token  
- Returns correct success and error responses  

---

## 🧩 User Info API — `GET /me`
- Protected endpoint  
- Requires valid JWT  
- Returns authenticated user details  

---
# Backend Task: Authentication Server

This project is a **basic authentication server** built using **Python FastAPI**. It allows users to **sign up**, **sign in**, and **access their own profile information** while following security best practices such as **password hashing** and **JWT-based authentication**. Instead of a database, user information is stored in a **JSON file** named `users.json`.

## POST /signup
To create a new user, send a POST request with a JSON body containing `username`, `password`, `fname` (first name), and `lname` (last name). For example:  
{"username": "exampleuser", "password": "Pass123", "fname": "John", "lname": "Doe"}  

**Success Response (201):**  
{"result": true, "message": "SignUp success. Please proceed to Signin"}  

**Failure Responses (400):**  
- Empty body or missing fields: {"result": false, "error": "fields can't be empty"}  
- Username validation failed (only lowercase letters, at least 4 characters): {"result": false, "error": "username check failed"}  
- Password validation failed (at least 1 uppercase, 1 lowercase, 1 number, no special characters, min 5 chars): {"result": false, "error": "password check failed"}  
- First/last name validation failed (letters only): {"result": false, "error": "fname or lname check failed"}  
- Username already exists: {"result": false, "error": "username already exists"}  

## POST /signin
To log in, send a POST request with `username` and `password`. Example:  
{"username": "exampleuser", "password": "Pass123"}  

**Success Response (200):**  
{"result": true, "jwt": "<jwt_token>", "message": "Signin success"}  

**Failure Responses (400):**  
- Empty body or missing fields: {"result": false, "error": "Please provide username and password"}  
- Invalid credentials: {"result": false, "error": "Invalid username/password"}  

## GET /user/me
To access your own profile, send a GET request with the Authorization header containing your JWT token: Authorization: Bearer <jwt_token>  

**Success Response (200):**  
{"result": true, "data": {"fname": "John", "lname": "Doe", "password": "<hashed_password>"}}  

**Failure Responses (400):**  
- Missing token: {"result": false, "error": "Please provide a JWT token"}  
- Invalid or expired token: {"result": false, "error": "JWT Verification Failed"}  

## How It Works
**Password Hashing:** User passwords are hashed using SHA-256 before storing in `users.json`. This ensures plain-text passwords are never stored.  

**JWT Authentication:** Upon successful sign-in, a JWT token is created with `username` and `fname`. Protected routes require this token to verify user identity.  

**File-based Storage:** Users are stored in a simple JSON file `users.json`. Functions `load_users()` and `save_users()` handle reading and writing safely.  

**Validation:** Input fields are validated using Python regex patterns. Invalid inputs return descriptive error messages with HTTP status 400.  

## Testing the Server
**Using Newman:** Install Newman globally using `npm install -g newman` and run the tests with `newman run --env-var baseUrl="http://127.0.0.1:8000" --env-var username="<your_username>" https://raw.githubusercontent.com/UXGorilla/hiring-backend/main/collection.json`  
  

This setup provides a **secure and simple authentication system** with FastAPI, JSON-based storage, password hashing, and JWT authentication, fully testable through Postman or Newman.


