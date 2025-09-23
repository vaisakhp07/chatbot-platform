import { useState } from "react";
import { api } from "../api/api";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      await api.post("/auth/signup", { email, password });
      alert("Signup successful. Please login.");
      navigate("/login");
    } catch (err) {
      alert("Signup failed");
    }
  };

  return (
    <div className="p-5">
      <h1 className="text-xl font-bold mb-4">Signup</h1>
      <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} className="border p-2 mb-2 w-full"/>
      <input type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} className="border p-2 mb-2 w-full"/>
      <button onClick={handleSignup} className="bg-blue-500 text-white p-2 w-full">Signup</button>
    </div>
  );
}
