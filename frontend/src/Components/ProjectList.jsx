// Location: src/components/ProjectList.jsx
import { useEffect, useState } from "react";
import { listProjects } from "../api/api";

export default function ProjectList() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    async function fetchProjects() {
      const data = await listProjects();
      setProjects(data);
    }
    fetchProjects();
  }, []);

  return (
    <div>
      <h2>Your Projects</h2>
      <ul>
        {projects.map((p) => (
          <li key={p.id}>{p.name}</li>
        ))}
      </ul>
    </div>
  );
}
