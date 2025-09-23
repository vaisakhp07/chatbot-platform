// Location: src/components/Signup.jsx
import { useState } from "react";
import { setToken } from "../utils/auth";

export default function Signup({ onSignup }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:8000/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (res.ok && data.access_token) {
        setToken(data.access_token);
        onSignup();
      } else {
        setError(data.detail || "Signup failed");
      }
    } catch (err) {
      setError("Network error");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
      <button type="submit">Signup</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}
