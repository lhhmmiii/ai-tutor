import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const ProtectedRoute = () => {
  const token = localStorage.getItem('access_token');
  

  if (!token) {
    // Nếu chưa có token, chuyển về login
    alert('Bạn cần đăng nhập để truy cập trang này');
    return <Navigate to="/login" replace />;
  }

  // Nếu có token, cho phép truy cập các route con
  return <Outlet />;
};

export default ProtectedRoute;
