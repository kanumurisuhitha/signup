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

## 🛠️ Tech Used
- FastAPI  
- Python  
- JOSE (JWT)  
- Hashlib  
- JSON-based storage  

---

## 🧪 Test Compatibility
This backend passes all tests in the official Newman Postman collection:

