const API_BASE_URL = import.meta.env.VITE_API_URL;

export async function login({ username, password }) {
    const res = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Login failed');
    return data;
  }
  
  export async function register({ username, email, fullName, password }) {
    const res = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username : username, email : email, full_name : fullName, password : password }),
    });
    
  
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Registration failed');
    return data;
  }
  
  export async function logout() {
    const token = localStorage.getItem('access_token');
    
    const res = await fetch(`${API_BASE_URL}/logout`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
  
    localStorage.removeItem('access_token');
    return "Logout successfully"
  }