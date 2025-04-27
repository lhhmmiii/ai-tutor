import React from 'react';
import { Routes, Route } from 'react-router-dom';

import GrammarCheck from '../pages/GrammarCheck';
import AnalyzeLevel from '../pages/AnalyzeLevel';
import WritingFeedback from '../pages/WritingFeedback';
import Vocabulary from '../pages/Vocabulary';
import Login from '../pages/Login';
import Register from '../pages/Register';

import MainLayout from '../layouts/MainLayout';
import AuthLayout from '../layouts/AuthLayout';
import ProtectedRoute from './ProtectedRoute';

function AppRoutes() {
  return (
    <Routes>
      {/* Routes có sidebar, được bảo vệ */}
      <Route element={<ProtectedRoute />}>
        <Route element={<MainLayout />}>
          <Route path="/" element={<GrammarCheck />} />
          <Route path="/analyze" element={<AnalyzeLevel />} />
          <Route path="/feedback" element={<WritingFeedback />} />
          <Route path="/vocabulary" element={<Vocabulary />} />
        </Route>
      </Route>

      {/* Routes không cần auth */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Route>
    </Routes>
  );
}

export default AppRoutes;
