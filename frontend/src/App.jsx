import { useState } from "react";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [chats, setChats] = useState([]); // store full chat history

  // Login function
  const login = async () => {
    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Login failed");
      }

      const data = await res.json();
      localStorage.setItem("access_token", data.access_token);
      alert("Login successful! Token saved.");
    } catch (error) {
      alert(error.message);
    }
  };

  // Send chat message
  const sendMessage = async () => {
    if (!message) return;
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch("http://localhost:8000/chats/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ project_id: 1, message }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Failed to send message");
      }

      const data = await res.json();

      // Add user message and bot response to chat history
      setChats((prev) => [
        ...prev,
        { sender: "You", message: data.message },
        { sender: "Bot", message: data.response },
      ]);

      setMessage(""); // clear input
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Login</h2>
      <input
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        placeholder="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={login}>Login</button>

      <h2>Chat</h2>
      <input
        placeholder="Enter message"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>

      <h3>Conversation:</h3>
      <div style={{ border: "1px solid #ccc", padding: "1rem", maxHeight: "300px", overflowY: "scroll" }}>
        {chats.map((c, idx) => (
          <div key={idx}>
            <b>{c.sender}:</b> {c.message}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
