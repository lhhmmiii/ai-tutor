import React, { useState } from 'react';
import { register } from '../services/auth_service';
import { useNavigate } from 'react-router-dom';

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: '',
    email: '',
    fullName: '',
    password: '',
    confirmPassword: '',
  });

  const handleChange = e => {
    setForm({...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    if (!form.username || !form.email || !form.fullName || form.password.length < 6) {
      alert('Please fill out all fields and ensure password is at least 6 characters');
      return;
    }
    if (form.password !== form.confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    try {
      const data = await register(form);
      alert(`Registration successful!\nUsername: ${form.username}\nEmail: ${form.email}`);
      setForm({ username: '', email: '', fullName: '', password: '', confirmPassword: '' });
      navigate('/');
    } catch (error) {
      alert(error.message || 'Registration failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-8">
      <form 
        onSubmit={handleSubmit} 
        className="bg-white p-8 rounded shadow-md w-full max-w-md"
      >
        <h2 className="text-3xl font-semibold mb-8 text-center text-blue-700">Register</h2>

        {/* Username input with icon */}
        <div className="relative mb-6">
          <span className="absolute inset-y-0 left-3 flex items-center text-blue-500">
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
            className="w-full pl-10 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {/* Email input with icon */}
        <div className="relative mb-6">
          <span className="absolute inset-y-0 left-3 flex items-center text-blue-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 12l-4 4m0 0l-4-4m4 4V8" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 18h16" />
            </svg>
          </span>
          <input 
            type="email" 
            name="email" 
            placeholder="Email" 
            value={form.email} 
            onChange={handleChange}
            className="w-full pl-10 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {/* Full Name input with icon */}
        <div className="relative mb-6">
          <span className="absolute inset-y-0 left-3 flex items-center text-blue-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.121 17.804A8.966 8.966 0 0112 15a8.966 8.966 0 016.879 2.804M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </span>
          <input 
            type="text" 
            name="fullName" 
            placeholder="Full Name" 
            value={form.fullName} 
            onChange={handleChange}
            className="w-full pl-10 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {/* Password input with icon */}
        <div className="relative mb-6">
          <span className="absolute inset-y-0 left-3 flex items-center text-blue-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11c1.657 0 3 1.343 3 3v3a3 3 0 11-6 0v-3c0-1.657 1.343-3 3-3z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 11V7a7 7 0 0114 0v4" />
            </svg>
          </span>
          <input 
            type="password" 
            name="password" 
            placeholder="Password (min 6 chars)" 
            value={form.password} 
            onChange={handleChange}
            className="w-full pl-10 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
            minLength={6}
          />
        </div>

        {/* Confirm Password input with icon */}
        <div className="relative mb-8">
          <span className="absolute inset-y-0 left-3 flex items-center text-blue-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11c1.657 0 3 1.343 3 3v3a3 3 0 11-6 0v-3c0-1.657 1.343-3 3-3z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 11V7a7 7 0 0114 0v4" />
            </svg>
          </span>
          <input 
            type="password" 
            name="confirmPassword" 
            placeholder="Confirm Password" 
            value={form.confirmPassword} 
            onChange={handleChange}
            className="w-full pl-10 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
            minLength={6}
          />
        </div>

        <button 
          type="submit" 
          className="w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700 transition font-semibold"
        >
          Register
        </button>

        <p className="mt-6 text-center text-gray-600 text-sm">
          Already have an account?{' '}
          <a href="/login" className="text-blue-600 hover:underline font-medium">Login</a>
        </p>
      </form>
    </div>
  );
}
