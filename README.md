# 🚀 Authentication Desk — FastAPI Backend

This project is a complete authentication system built using **FastAPI** for the **UX Gorilla Hiring Backend Task**. It includes user signup, login, and authenticated user retrieval with strict validations and JWT-based authentication. The project is designed to pass the official Newman Postman test collection with **0 assertion errors**.

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
This project is a basic authentication server built using Python FastAPI. It allows users to sign up, sign in, and access their own profile information while following security best practices such as password hashing and JWT-based authentication. Instead of a database, user information is stored in a JSON file named `users.json` to keep things simple and file-based.

POST /signup  
To create a new user, send a POST request with a JSON body containing the following fields: `username`, `password`, `fname` (first name), and `lname` (last name).  

Request Body (application/json):  
{
  "username": "exampleuser",
  "password": "Pass123",
  "fname": "John",
  "lname": "Doe"
}  

Success Response (201):  
If all fields are valid and the username does not already exist, the server responds with:  
{
  "result": true,
  "message": "SignUp success. Please proceed to Signin"
}  

Failure Responses (400):  
- If the request body is empty or any required field is missing:  
{
  "result": false,
  "error": "fields can't be empty"
}  
- If the username is invalid (must contain only lowercase letters and be at least 4 characters):  
{
  "result": false,
  "error": "username check failed"
}  
- If the password is invalid (must contain at least 1 uppercase letter, 1 lowercase letter, 1 number, no special characters, and be at least 5 characters long):  
{
  "result": false,
  "error": "password check failed"
}  
- If the first or last name contains invalid characters (must be only letters):  
{
  "result": false,
  "error": "fname or lname check failed"
}  
- If the username already exists:  
{
  "result": false,
  "error": "username already exists"
}  

POST /signin  
To log in, send a POST request with your `username` and `password`.  

Request Body (application/json):  
{
  "username": "exampleuser",
  "password": "Pass123"
}  

Success Response (200):  
On successful login, the server responds with a JWT token in the response:  
{
  "result": true,
  "jwt": "<jwt_token>",
  "message": "Signin success"
}  

Failure Responses (400):  
- If the request body is empty or fields are missing:  
{
  "result": false,
  "error": "Please provide username and password"
}  
- If the username or password is invalid:  
{
  "result": false,
  "error": "Invalid username/password"
}  

GET /user/me  
To access your own profile, send a GET request with the **Authorization** header containing your JWT token received from `/signin`.  

Headers:  
Authorization: Bearer <jwt_token>  

Success Response (200):  
If the token is valid, the server returns the user’s profile information including hashed password:  
{
  "result": true,
  "data": {
    "fname": "John",
    "lname": "Doe",
    "password": "<hashed_password>"
  }
}  

Failure Responses (400):  
- If the JWT token is missing:  
{
  "result": false,
  "error": "Please provide a JWT token"
}  
- If the JWT token is invalid or expired:  
{
  "result": false,
  "error": "JWT Verification Failed"
}  

How It Works  
Password Hashing: All passwords are hashed using **SHA-256** before storing in `users.json`. This ensures that no plain-text passwords are stored, increasing security.  

JWT Authentication: When a user successfully signs in, a JWT token is created containing the `username` and `fname`. This token must be sent in the Authorization header for protected routes to verify user identity.  

File-based Storage: All user data is stored in a simple JSON file named `users.json`. The functions `load_users()` and `save_users()` safely handle reading from and writing to this file.  

Validation: Input fields are validated using Python regex patterns. If a user provides invalid data, the server returns descriptive error messages with HTTP status 400.  

Testing the Server  
Using Newman (Command Line):  
1. Install Newman globally using `npm install -g newman`.  
2. Run the test cases with:  
```bash
newman run --env-var baseUrl="http://127.0.0.1:8000" --env-var username="<your_username>" https://raw.githubusercontent.com/UXGorilla/hiring-backend/main/collection.json


