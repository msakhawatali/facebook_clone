# 📘 Facebook Clone

A backend API for a Facebook-style social media app, built with **FastAPI** and **PostgreSQL**.
This project includes core features like OAuth2 login, post and comment functionality, and friend requests.

---

## 🔐 Features

* **User Authentication**

  * Signup
  * Login with **OAuth2 & JWT (Bearer Token)**
  * Secure password hashing

* **Posts**

  * Create Post
  * Edit Post
  * Delete Post

* **Comments**

  * Add Comment
  * Edit Comment
  * Delete Comment

* **Friend System**

  * Send/Add Friend Requests

---

## 🛠️ Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* OAuth2 + JWT (token-based auth)
* Passlib (for password hashing)

---

## 🚀 How to Set Up the Project

Follow these steps to run the project locally:

### 1. Clone the repository

```bash
git clone https://github.com/your_username/facebook_clone.git
cd facebook_clone
```

### 2. Create and activate virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database

* Make sure **PostgreSQL** is installed and running
* Create a database (example: `facebook_clone`)
* Update your **`.env`** or `settings.py` file with the database URL

Example:

```
DATABASE_URL=postgresql://username:password@localhost/facebook_clone
```

### 5. Run the FastAPI server

```bash
uvicorn main:app --reload
```

* Go to: `http://localhost:8000/docs` to access the Swagger UI and test the API.

---

## 📦 Future Improvements

* Accept/reject friend requests
* Like system for posts/comments
* User profile page
* Notifications

---

## 📌 License

This project is for educational purposes and open to contributions.
