# Chatbot Platform (Minimal Version)

A minimal version of a **Chatbot Platform** built with **FastAPI** (backend) and **React** (frontend). Users can register, log in, create projects/agents, and interact with an AI-powered chatbot.

> ⚠️ Note: This is a work-in-progress project. Some features described in the original specification are not yet fully implemented.

---

## Features Implemented

### Authentication & User Management
- User registration and login using **JWT tokens**
- Password hashing and verification
- Protected routes for chat access

### Projects / Agents
- Create projects associated with a user
- Associate prompts/messages with a project
- Each project can have multiple chat sessions

### Chat Interface
- Simple frontend in React
- Chat with AI-powered agent
- Uses **OpenAI GPT API** for responses
- Token-based authorization to secure chat API

---

## Features Pending / Not Yet Implemented

- File upload and management using OpenAI Files API
- Advanced analytics or integrations
- Full project dashboard
- UI improvements and better frontend styling
- OAuth2 or additional authentication flows
- Multi-agent support per user

---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, Python 3.10+
- **Frontend:** React, Vite
- **AI Integration:** OpenAI GPT API
- **Authentication:** JWT tokens
- **Environment Management:** dotenv

---

## Setup Instructions

### Backend

1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd chatbot-platform
