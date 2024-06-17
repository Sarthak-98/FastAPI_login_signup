# FastAPI_login_signup
Sign up and Login system in FastAPI Python and Database is PostgreSQL. 

```markdown
# FastAPI Signup and Login Backend System

This project is a backend system API for user signup and login, built using FastAPI and PostgreSQL. 

## Features

- User Signup: Register a new user with a username and password.
- User Login: Authenticate a user and provide a token for access.
- JWT Authentication: Secure endpoints using JSON Web Tokens.
- Password Hashing: Secure password storage using hashing.

## Tech Stack

- **FastAPI**: The web framework for building APIs.
- **PostgreSQL**: The relational database management system.
- **SQLAlchemy**: The ORM used for database interactions.
- **Pydantic**: Data validation and settings management.
- **JWT**: JSON Web Tokens for secure user authentication.

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**

   Update the database configuration in the `.env` file with your PostgreSQL database credentials.

5. **Run database migrations**

   Ensure your PostgreSQL server is running, then run:

   ```bash
   alembic upgrade head
   ```

6. **Start the FastAPI server**

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000` after you add this url to the cors origin in the ".env" file

## API Endpoints

### Signup

- **URL**: `/signup`
- **Method**: `POST`
- **Request Body**:

  ```json
  {
    "username": "your-username",
    "password": "your-password"
  }
  ```

- **Response**:

  ```json
  {
    "msg": "User created successfully"
  }
  ```

### Login

- **URL**: `/login`
- **Method**: `POST`
- **Request Body**:

  ```json
  {
    "username": "your-username",
    "password": "your-password"
  }
  ```

- **Response**:

  ```json
  {
    "access_token": "your-jwt-token",
    "token_type": "bearer"
  }
  ```

### Protected Endpoint Example

- **URL**: `/protected`
- **Method**: `GET`
- **Headers**:

  ```http
  Authorization: Bearer your-jwt-token
  ```

- **Response**:

  ```json
  {
    "msg": "You are logged in!"
  }
  ```

## Folder Structure

```
.
├── alembic/               # Database migrations
├── app/
│   ├── __init__.py
│   ├── main.py            # Main application entry point
│   ├── database.py         
│   ├── log_config.py
|   ├── core/
|       ├── __init__.py
|       ├── config.py          
├── authentication/                 
│   ├── __init__.py
│   ├── models/
|       ├── __init.py__
|       ├── user.py
|   ├── routs/
|       ├── __init.py__
|       ├── user.py
|   ├── schemas/
|       ├── __init.py__
|       ├── user.py
|   ├── utils/
|       ├── __init.py__
|       ├── auth_handler.py
|       ├── change_pass.py
|       ├── user_login.py
|       ├── email_util.py
|       ├── user_signup.py
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## Contact

For any inquiries or support, please contact [your-email@example.com].

---

Thank you for using this project! Happy coding!
```

Replace placeholders like `your-username`, `your-repo-name`, and `your-email@example.com` with your actual details. Additionally, ensure you include the `LICENSE` file in your repository if you mention it in the README.
