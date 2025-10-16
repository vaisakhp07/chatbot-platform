# Chatbot Platform 🚀

A full-stack **Chatbot Platform** built with **FastAPI** (backend) and **React** (frontend), featuring modern DevOps practices including Docker, CI/CD, and automated deployments.

## 🏗️ Architecture

### Tech Stack
- **Backend:** FastAPI, SQLAlchemy, SQLite/PostgreSQL, Python 3.11
- **Frontend:** React, Vite, CSS3
- **AI Integration:** OpenRouter GPT-3.5 Turbo
- **Authentication:** JWT tokens
- **Database:** SQLite (Development), PostgreSQL (Production)
- **DevOps:** Docker, Docker Compose, GitHub Actions, Nginx

## 🚀 Features

### ✅ Implemented
- **User Authentication** - JWT-based registration/login
- **Project Management** - Create and manage chat projects
- **AI-Powered Chat** - Real-time conversations with GPT-3.5
- **Chat Persistence** - Messages survive logout/login cycles
- **Containerized** - Docker support for development and production
- **CI/CD Pipeline** - Automated testing and deployment

### 🔄 In Progress
- File upload and management
- Advanced analytics dashboard
- Multi-agent support
- Production deployment automation

## 🛠️ Quick Start

### Prerequisites
- Docker & Docker Compose
- OpenRouter API Key ([Get one here](https://openrouter.ai/))

### Development with Docker
```bash
# Clone the repository
git clone https://github.com/yourusername/chatbot-platform
cd chatbot-platform

# Create environment file
echo "OPENAI_API_KEY=your-openrouter-key-here" > .env

# Start development environment
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
