import requests
import uuid

BASE_URL = "http://127.0.0.1:8000"

# 1️⃣ Signup
signup_data = {
    "email": f"testuser_{uuid.uuid4().hex[:8]}@example.com",
    "password": "testpassword"
}

signup_resp = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
print("Signup Response:", signup_resp.json())

# 2️⃣ Login
login_data = {
    "email": signup_data["email"],
    "password": signup_data["password"]
}

login_resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)
login_json = login_resp.json()
print("Login Response:", login_json)

if "access_token" not in login_json:
    raise Exception("Login failed. Cannot test protected endpoints.")

token = login_json["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 3️⃣ Create Project
project_data = {
    "name": "Test Project",
    "description": "This is a test project"
}

project_resp = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
print("Create Project Response:", project_resp.json())

project_id = project_resp.json().get("id")

# 4️⃣ List Projects
list_projects_resp = requests.get(f"{BASE_URL}/projects/", headers=headers)
print("List Projects Response:", list_projects_resp.json())

# 5️⃣ Send Chat
chat_data = {
    "message": "Hello, chatbot!",
    "project_id": project_id
}

chat_resp = requests.post(f"{BASE_URL}/chats/", json=chat_data, headers=headers)
print("Send Chat Response:", chat_resp.json())

# 6️⃣ List Chats
list_chats_resp = requests.get(f"{BASE_URL}/chats/", headers=headers)
print("List Chats Response:", list_chats_resp.json())
