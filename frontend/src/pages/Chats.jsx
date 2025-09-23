import React, { useEffect, useState } from "react";
import { listChats, sendMessage } from "../api/chat";

export default function Chat() {
  const [chats, setChats] = useState([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const fetchChats = async () => {
    try {
      const data = await listChats();
      setChats(data);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchChats();
  }, []);

  const handleSend = async () => {
    if (!message) return;
    try {
      const res = await sendMessage(message);
      setChats([...chats, { message: res.message, sender: "user" }, { message: res.response, sender: "bot" }]);
      setMessage("");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h2>Chatbot</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <div style={{ border: "1px solid #ccc", padding: "10px", height: "300px", overflowY: "scroll" }}>
        {chats.map((c, idx) => (
          <div key={idx}>
            <b>{c.sender || "User"}:</b> {c.message}
          </div>
        ))}
      </div>
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
