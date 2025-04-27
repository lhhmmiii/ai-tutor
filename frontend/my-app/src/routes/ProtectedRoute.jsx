import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const ProtectedRoute = () => {
  const token = localStorage.getItem('access_token');

  if (!token) {
    // Nếu chưa có token, chuyển về login
    return <Navigate to="/login" replace />;
  }

  // Nếu có token, cho phép truy cập các route con
  return <Outlet />;
};

export default ProtectedRoute;
