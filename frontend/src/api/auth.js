// src/api/auth.js
export async function login(email, password) {
  const res = await fetch("http://localhost:8000/api/auth/login", {  // ADD /api
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    throw new Error("Invalid email or password");
  }

  return res.json();
}
