# Secure Notes App

A secure backend web application built with FastAPI, Docker, and Microsoft Azure.

The project allows users to register, authenticate using JWT tokens, and securely store encrypted notes in a database.

## Features

- User registration and login
- JWT authentication
- Password hashing with bcrypt
- Encrypted notes using Fernet encryption
- CRUD operations for notes
- Docker containerization
- Azure Container Apps deployment
- Swagger API documentation
- SQLite database with SQLAlchemy ORM
- Environment variables with `.env`

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Docker
- Azure Container Apps
- Azure Container Registry
- JWT
- bcrypt
- cryptography (Fernet)

---

## Project Structure

```bash
secure_azure_app/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── notes.db
│
├── frontend/
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
Local Setup
Clone the repository
git clone <repo-url>
cd secure_azure_app
Create virtual environment
python3 -m venv venv
Activate virtual environment

Mac/Linux:

source venv/bin/activate

Windows:

venv\Scripts\activate
Install dependencies
pip install -r requirements.txt
Run the app
uvicorn app.main:app --reload

Swagger docs:

http://127.0.0.1:8000/docs
Docker
Build image
docker build -t secure-notes-app .
Run container
docker run --env-file .env -p 8000:8000 secure-notes-app
Azure Deployment

The application was deployed using:

Azure Container Registry (ACR)
Azure Container Apps

Deployment included:

Docker image push to Azure
Environment variables configuration
Public HTTPS endpoint
Cloud-hosted FastAPI backend
Security Features
JWT token authentication
Password hashing with bcrypt
Encrypted note storage using Fernet
Environment secrets stored outside source code
HTTPS endpoint on Azure
API Endpoints
Method	Endpoint	Description
GET	/	Root endpoint
GET	/notes	Get user notes
POST	/notes	Create note
PUT	/notes	Modify note
DELETE	/notes	Delete note
DELETE	/notes/all	Delete all notes
POST	/register	Register user
POST	/login	Login user
Future Improvements
PostgreSQL integration
Azure Key Vault
CI/CD with GitHub Actions
Rate limiting
Elasticsearch logging
Frontend deployment
Role-based authentication
Author

Denis
Computer Science & IT Engineering Student
