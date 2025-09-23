import React, { useEffect, useState } from "react";
import { listProjects, createProject } from "../api/api";
import { useNavigate } from "react-router-dom";

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      try {
        const res = await listProjects(); // calls backend via axios
        setProjects(res);
      } catch (err) {
        console.error(err);
        setError("Failed to fetch projects");
      }
    })();
  }, []);

  const handleCreate = async () => {
    if (!title) return;
    try {
      const res = await createProject(title);
      setProjects((prev) => [...prev, res]);
      setTitle("");
    } catch (err) {
      console.error(err);
      setError("Failed to create project");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Projects</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <div>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New project title"
        />
        <button onClick={handleCreate}>Create Project</button>
      </div>

      <ul>
        {projects.map((p) => (
          <li key={p.id}>
            {p.title}{" "}
            <button onClick={() => navigate("/chats")}>Open Chat</button>
          </li>
        ))}
      </ul>
    </div>
  );
}