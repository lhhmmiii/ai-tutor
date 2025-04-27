const API_BASE_URL = 'http://127.0.0.1:8000';

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
  
  export async function register({ username, email, password }) {
    const res = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password }),
    });
  
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Registration failed');
    return data;
  }
  
  export function logout() {
    // Nếu backend có logout API, bạn có thể gọi ở đây
    // Hiện tại chỉ xóa localStorage token
    localStorage.removeItem('token');
  }