import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [user, setUser] = useState(null);
    const [email, setEmail] = useState('test@example.com');
    const [password, setPassword] = useState('password123');
    const [loading, setLoading] = useState(false);
    
    // Navigation state
    const [activeSection, setActiveSection] = useState('chat'); // 'chat' or 'projects'
    
    // Project states
    const [projects, setProjects] = useState([]);
    const [showProjectModal, setShowProjectModal] = useState(false);
    const [projectForm, setProjectForm] = useState({ name: '', description: '' });
    
    // Chat states (main chat interface)
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [chatLoading, setChatLoading] = useState(false);
    const [chatHistory, setChatHistory] = useState([]);
    const [currentChatId, setCurrentChatId] = useState(null);

    // Load projects and chat history when user logs in
    useEffect(() => {
        const token = localStorage.getItem('token');
        const userData = localStorage.getItem('user');
        if (token && userData) {
            const parsedUser = JSON.parse(userData);
            setUser(parsedUser);
        }
    }, []);
    
    // Load projects after user state is set
    useEffect(() => {
        if (user) {
            loadProjects();
            loadChatHistory();
        }
    }, [user]);

    const loadProjects = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                console.error('No token found');
                return;
            }
            
            const response = await fetch('/api/projects/', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (response.status === 401) {
                handleLogout();
                alert('Session expired. Please login again.');
                return;
            }
            
            if (response.ok) {
                const data = await response.json();
                setProjects(data);
            } else {
                console.error('Failed to load projects:', response.status);
            }
        } catch (error) {
            console.error('Error loading projects:', error);
        }
    };

    const loadChatHistory = async () => {
        try {
            const token = localStorage.getItem('token');
            console.log('Loading chat history...');
            
            // Load projects first to get project IDs
            const projectsResponse = await fetch('/api/projects/', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (projectsResponse.ok) {
                const projects = await projectsResponse.json();
                console.log('Projects loaded:', projects);
                
                // Load chat history from ALL projects
                const allChats = [];
                
                for (const project of projects) {
                    console.log('Loading history for project:', project.id);
                    const historyResponse = await fetch(`/api/chat/history/${project.id}`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    
                    if (historyResponse.ok) {
                        const messages = await historyResponse.json();
                        console.log(`Messages for project ${project.id}:`, messages);
                        
                        // Convert database messages to chat format
                        if (messages.length > 0) {
                            const chat = {
                                id: `project-${project.id}`,
                                title: project.name,
                                messages: messages.map(msg => ({
                                    role: msg.message_type,
                                    content: msg.message_type === 'user' ? msg.message : msg.response
                                })),
                                createdAt: project.created_at,
                                projectId: project.id
                            };
                            allChats.push(chat);
                        }
                    } else {
                        console.log('Failed to load history for project:', project.id);
                    }
                }
                
                console.log('All chats:', allChats);
                setChatHistory(allChats);
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    email: email, 
                    password: password 
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                setUser(data.user);
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('user', JSON.stringify(data.user));
                await loadProjects();
                loadChatHistory();
            } else {
                const errorText = await response.text();
                alert('Login failed: ' + errorText);
            }
        } catch (error) {
            alert('Network error: ' + error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        setUser(null);
        setProjects([]);
        setMessages([]);
        setChatHistory([]);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('chatHistory');
    };

    // Main Chat Function
    const sendMessage = async (e) => {
        e.preventDefault();
        if (!newMessage.trim()) return;
    
        const userMessage = { role: 'user', content: newMessage };
        const updatedMessages = [...messages, userMessage];
        setMessages(updatedMessages);
        setNewMessage('');
        setChatLoading(true);
    
        try {
            const token = localStorage.getItem('token');
            
            let projectId;
            
            // If no current chat ID, we need to create a project first
            if (!currentChatId) {
                const projectResponse = await fetch('/api/projects/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        name: `Chat ${new Date().toLocaleString()}`,
                        description: 'Chat conversation'
                    })
                });
                
                if (projectResponse.ok) {
                    const newProject = await projectResponse.json();
                    projectId = newProject.id;
                    setProjects([newProject, ...projects]);
                    
                    const newChat = {
                        id: `project-${newProject.id}`,
                        title: newProject.name,
                        messages: [],
                        projectId: newProject.id
                    };
                    setChatHistory([newChat, ...chatHistory]);
                    setCurrentChatId(newChat.id);
                }
            } else {
                // Use the current project
                projectId = parseInt(currentChatId.replace('project-', ''));
            }
    
            if (!projectId) {
                throw new Error('No project available');
            }
    
            // Send the message
            const response = await fetch('/api/chat/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    message: newMessage,
                    project_id: projectId
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                const aiMessage = { role: 'assistant', content: data.response };
                const finalMessages = [...updatedMessages, aiMessage];
                setMessages(finalMessages);
                
                // Update chat history with new messages
                await loadChatHistory();
                
            } else {
                const errorText = await response.text();
                alert('Error: ' + errorText);
                setMessages(messages);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            alert('Network error: ' + error.message);
            setMessages(messages);
        } finally {
            setChatLoading(false);
        }
    };

    const loadChat = async (chat) => {
        try {
            const token = localStorage.getItem('token');
            
            // Load fresh messages from database for this project
            const response = await fetch(`/api/chat/history/${chat.projectId}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (response.ok) {
                const messages = await response.json();
                const formattedMessages = messages.map(msg => ({
                    role: msg.message_type,
                    content: msg.message_type === 'user' ? msg.message : msg.response
                }));
                
                setMessages(formattedMessages);
                setCurrentChatId(chat.id);
            }
        } catch (error) {
            console.error('Error loading chat:', error);
            // Fallback to cached messages
            setMessages(chat.messages);
            setCurrentChatId(chat.id);
        }
    };

    const startNewChat = async () => {
        try {
            const token = localStorage.getItem('token');
            
            // Create a new project for the new chat
            const projectResponse = await fetch('/api/projects/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    name: `Chat ${new Date().toLocaleString()}`,
                    description: 'New chat conversation'
                })
            });
            
            if (projectResponse.ok) {
                const newProject = await projectResponse.json();
                
                // Add to projects list
                setProjects([newProject, ...projects]);
                
                // Create empty chat entry
                const newChat = {
                    id: `project-${newProject.id}`,
                    title: newProject.name,
                    messages: [],
                    projectId: newProject.id
                };
                
                // Add to chat history
                setChatHistory([newChat, ...chatHistory]);
                
                // Set as current chat
                setCurrentChatId(newChat.id);
                setMessages([]);
                setNewMessage('');
                
                console.log('New chat created with project:', newProject.id);
            }
        } catch (error) {
            console.error('Error creating new chat:', error);
            alert('Failed to create new chat');
        }
    };

    // REMOVE THIS DUPLICATE FUNCTION - KEEP ONLY THE ONE ABOVE
    // const loadChat = (chat) => {
    //     setMessages(chat.messages);
    //     setCurrentChatId(chat.id);
    // };

    const deleteChat = (chatId, e) => {
        e.stopPropagation();
        const updatedHistory = chatHistory.filter(chat => chat.id !== chatId);
        setChatHistory(updatedHistory);
        localStorage.setItem('chatHistory', JSON.stringify(updatedHistory));
        
        if (currentChatId === chatId) {
            startNewChat();
        }
    };

    const createProject = async (e) => {
        e.preventDefault();
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/projects/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(projectForm)
            });
            if (response.ok) {
                const newProject = await response.json();
                setProjects([...projects, newProject]);
                setShowProjectModal(false);
                setProjectForm({ name: '', description: '' });
            }
        } catch (error) {
            console.error('Error creating project:', error);
            alert('Error creating project');
        }
    };

    // ... rest of your component (return statement) remains the same ...

    if (!user) {
        return (
            <div className="auth-container">
                <div className="auth-form">
                    <h2>Login</h2>
                    <form onSubmit={handleLogin}>
                        <input 
                            type="email" 
                            placeholder="Email"
                            value={email} 
                            onChange={(e) => setEmail(e.target.value)} 
                            required 
                        />
                        <input 
                            type="password" 
                            placeholder="Password"
                            value={password} 
                            onChange={(e) => setPassword(e.target.value)} 
                            required 
                        />
                        <button type="submit" disabled={loading}>
                            {loading ? 'Logging in...' : 'Login'}
                        </button>
                    </form>
                    <div style={{ marginTop: '20px', padding: '10px', background: '#f5f5f5' }}>
                        <p><strong>Test Credentials:</strong></p>
                        <p>Email: test@example.com</p>
                        <p>Password: password123</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="app">
            {/* Sidebar */}
            <div className="sidebar">
                <div className="sidebar-header">
                    <button onClick={startNewChat} className="new-chat-btn">
                        + New chat
                    </button>
                </div>
                
                <div className="chat-history">
                    {chatHistory.map(chat => (
                        <div 
                            key={chat.id}
                            className={`chat-history-item ${currentChatId === chat.id ? 'active' : ''}`}
                            onClick={() => loadChat(chat)}
                        >
                            <span className="chat-title">💬 {chat.title}</span>
                            <button 
                                className="delete-chat"
                                onClick={(e) => deleteChat(chat.id, e)}
                            >
                                ×
                            </button>
                        </div>
                    ))}
                </div>

                <div className="sidebar-footer">
                    <button 
                        className={`nav-button ${activeSection === 'chat' ? 'active' : ''}`}
                        onClick={() => setActiveSection('chat')}
                    >
                        💬 Chats
                    </button>
                    <button 
                        className={`nav-button ${activeSection === 'projects' ? 'active' : ''}`}
                        onClick={() => setActiveSection('projects')}
                    >
                        📁 Projects
                    </button>
                    <div className="user-info-sidebar">
                        <span>{user.name}</span>
                        <button onClick={handleLogout}>Logout</button>
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <div className="main-content">
                {/* Chat Section (Default) */}
                {activeSection === 'chat' && (
                    <div className="chat-section">
                        <div className="chat-container">
                            {messages.length === 0 ? (
                                <div className="empty-chat">
                                    <h1>Chatbot Platform</h1>
                                    <p>Start a conversation or select a previous chat from the sidebar.</p>
                                </div>
                            ) : (
                                <div className="messages-container">
                                    {messages.map((message, index) => (
                                        <div key={index} className={`message ${message.role}`}>
                                            <div className="message-content">
                                                {message.content}
                                            </div>
                                        </div>
                                    ))}
                                    {chatLoading && (
                                        <div className="message assistant">
                                            <div className="message-content typing">
                                                Thinking...
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}
                            
                            <form onSubmit={sendMessage} className="message-form">
                                <input
                                    type="text"
                                    value={newMessage}
                                    onChange={(e) => setNewMessage(e.target.value)}
                                    placeholder="Message Chatbot Platform..."
                                    disabled={chatLoading}
                                />
                                <button type="submit" disabled={chatLoading || !newMessage.trim()}>
                                    Send
                                </button>
                            </form>
                        </div>
                    </div>
                )}

                {/* Projects Section */}
                {activeSection === 'projects' && (
                    <div className="projects-section">
                        <div className="projects-header">
                            <h1>Projects</h1>
                            <button onClick={() => setShowProjectModal(true)}>+ New Project</button>
                        </div>
                        
                        <div className="projects-grid">
                            {projects.map(project => (
                                <div key={project.id} className="project-card">
                                    <h3>{project.name}</h3>
                                    {project.description && <p>{project.description}</p>}
                                    <div className="project-actions">
                                        <button>Open</button>
                                        <button>Settings</button>
                                    </div>
                                </div>
                            ))}
                            
                            {projects.length === 0 && (
                                <div className="empty-projects">
                                    <p>No projects yet. Create your first project to get started!</p>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>

            {/* Project Creation Modal */}
            {showProjectModal && (
                <div className="modal">
                    <div className="modal-content">
                        <span className="close" onClick={() => setShowProjectModal(false)}>×</span>
                        <h3>Create New Project</h3>
                        <form onSubmit={createProject}>
                            <input
                                type="text"
                                placeholder="Project Name"
                                value={projectForm.name}
                                onChange={(e) => setProjectForm(prev => ({ ...prev, name: e.target.value }))}
                                required
                            />
                            <textarea
                                placeholder="Description"
                                value={projectForm.description}
                                onChange={(e) => setProjectForm(prev => ({ ...prev, description: e.target.value }))}
                                rows="3"
                            />
                            <button type="submit">Create Project</button>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;