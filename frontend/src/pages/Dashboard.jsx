import { useEffect, useState } from "react";
import { api, setAuthToken } from "../api/api";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const [projects, setProjects] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) navigate("/login");
    setAuthToken(token);
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    const res = await api.get("/projects/");
    setProjects(res.data);
  };

  return (
    <div className="p-5">
      <h1 className="text-xl font-bold mb-4">Dashboard</h1>
      <ul>
        {projects.map(p => (
          <li key={p.id} className="mb-2">
            <span>{p.name}</span>
            <button onClick={()=>navigate(`/project/${p.id}`)} className="ml-2 bg-blue-500 text-white p-1">Open</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
