const API_URL = "http://localhost:8000";

export async function listChats() {
  const token = localStorage.getItem("access_token");
  const res = await fetch(`${API_URL}/chats/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch chats");
  return res.json();
}

export async function sendMessage(message, project_id = 1) {
  const token = localStorage.getItem("access_token");
  const res = await fetch(`${API_URL}/chats/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ message, project_id }),
  });
  if (!res.ok) throw new Error("Failed to send message");
  return res.json();
}
