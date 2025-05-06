import React, { useState } from 'react';
import { login } from '../services/auth_service'
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: '',
    password: ''
  });

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    if (!form.username || !form.password) {
      alert('Please fill out all fields');
      return;
    }
    try {
      const data = await login(form);
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('user_id', data.user_id)
      setForm({ username: '', password: '' });
      navigate('/');
    } catch (error) {
      alert(error.message);
    }
    
  };

  return (
    <div className="min-h-screen flex bg-gray-100 items-center justify-center p-8">
      <form 
        onSubmit={handleSubmit} 
        className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md"
      >
        <h2 className="text-3xl font-bold mb-8 text-center text-indigo-700">Welcome Back</h2>

        {/* Username input with icon */}
        <div className="relative mb-6">
          <span className="absolute inset-y-0 left-3 flex items-center text-indigo-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.121 17.804A8.966 8.966 0 0112 15a8.966 8.966 0 016.879 2.804M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </span>
          <input 
            type="text" 
            name="username" 
            placeholder="Username" 
            value={form.username} 
            onChange={handleChange}
            className="w-full pl-10 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        {/* Password input with icon */}
        <div className="relative mb-8">
          <span className="absolute inset-y-0 left-3 flex items-center text-indigo-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11c1.657 0 3 1.343 3 3v3a3 3 0 11-6 0v-3c0-1.657 1.343-3 3-3z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 11V7a7 7 0 0114 0v4" />
            </svg>
          </span>
          <input 
            type="password" 
            name="password" 
            placeholder="Password" 
            value={form.password} 
            onChange={handleChange}
            className="w-full pl-10 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>

        <button 
          type="submit" 
          className="w-full bg-indigo-600 text-white py-3 rounded hover:bg-indigo-700 transition font-semibold"
        >
          Login
        </button>

        <p className="mt-6 text-center text-gray-600">
          Don't have an account?{' '}
          <a href="/register" className="text-indigo-600 hover:underline font-medium">
            Register
          </a>
        </p>
      </form>
    </div>
  );
}
