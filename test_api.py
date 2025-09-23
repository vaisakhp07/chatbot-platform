# test_api.py
import requests

BASE_URL = "http://127.0.0.1:8000"

# ----------------------------
# Test Signup
# ----------------------------
signup_data = {
    "email": "testuser@example.com",
    "password": "test123"
}
resp = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
print("Signup Response:", resp.json())

# ----------------------------
# Test Login
# ----------------------------
login_data = {
    "email": "testuser@example.com",
    "password": "test123"
}
login_resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)
login_json = login_resp.json()
print("Login Response:", login_json)

if "access_token" not in login_json:
    raise Exception("Login failed, cannot continue tests")

# Store token
token = login_json["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# ----------------------------
# Create Project
# ----------------------------
project_data = {"name": "Test Project", "description": "This is a test project"}
proj_resp = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
print("Create Project Response:", proj_resp.json())
project_id = proj_resp.json()["id"]

# ----------------------------
# List Projects
# ----------------------------
list_proj = requests.get(f"{BASE_URL}/projects/", headers=headers)
print("List Projects Response:", list_proj.json())

# ----------------------------
# Send Chat
# ----------------------------
chat_data = {"message": "Hello, chatbot!", "project_id": project_id}
chat_resp = requests.post(f"{BASE_URL}/chats/", json=chat_data, headers=headers)
print("Send Chat Response:", chat_resp.json())

# ----------------------------
# List Chats
# ----------------------------
chats_resp = requests.get(f"{BASE_URL}/chats/", headers=headers)
print("List Chats Response:", chats_resp.json())

# ----------------------------
# File Upload
# ----------------------------
files = {"file": open("sample.txt", "rb")}  # create a sample.txt file
upload_resp = requests.post(f"{BASE_URL}/files/upload?project_id={project_id}", files=files, headers=headers)
print("File Upload Response:", upload_resp.json())

# ----------------------------
# List Files
# ----------------------------
list_files_resp = requests.get(f"{BASE_URL}/files/?project_id={project_id}", headers=headers)
print("List Files Response:", list_files_resp.json())
