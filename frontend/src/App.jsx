import { useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    const res = await axios.post("http://localhost:8000/api/chat/", {
      user_message: message,
    });
    setChat([...chat, { role: "user", text: message }, { role: "assistant", text: res.data.assistant }]);
    setMessage("");
  };

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Chatbot Platform</h1>
      <div className="border p-4 h-96 overflow-y-auto">
        {chat.map((c, i) => (
          <p key={i} className={c.role === "user" ? "text-blue-600" : "text-green-600"}>
            <strong>{c.role}:</strong> {c.text}
          </p>
        ))}
      </div>
      <div className="mt-4 flex">
        <input
          className="border flex-grow p-2"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type a message..."
        />
        <button onClick={sendMessage} className="bg-blue-500 text-white px-4">
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
