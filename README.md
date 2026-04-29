# E-Commerce Platform — User Service

A production-ready User Service built with FastAPI and PostgreSQL, 
part of a larger microservices-based e-commerce platform.

## Tech Stack
- Python 3.12 / FastAPI
- PostgreSQL
- SQLAlchemy ORM
- JWT Authentication (python-jose)
- Password Hashing (bcrypt/passlib)
- Pydantic v2

## Features
- User registration with duplicate email/username validation
- Secure login with JWT token generation
- Protected routes using Bearer token authentication
- Profile management (view, update, deactivate)
- Role-based access control (admin/customer)
- Soft delete — accounts are deactivated not permanently deleted
- Password hashing with bcrypt — plain passwords never stored

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /users/register | No | Register a new user |
| POST | /users/login | No | Login and receive JWT token |
| GET | /users/profile | Yes | Get current user profile |
| PUT | /users/update | Yes | Update profile details |
| DELETE | /users/delete | Yes | Deactivate account |
| GET | /users | Yes (Admin) | Get all active users |

