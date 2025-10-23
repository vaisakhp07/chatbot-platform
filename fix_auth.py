# Script to update the auth.py file
with open('app/api/auth.py', 'r') as f:
    content = f.read()

# Replace bcrypt with pbkdf2_sha256
content = content.replace(
    'pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")',
    'pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")'
)

# Write the updated content back
with open('app/api/auth.py', 'w') as f:
    f.write(content)

print("✅ Updated auth.py to use pbkdf2_sha256 instead of bcrypt")
