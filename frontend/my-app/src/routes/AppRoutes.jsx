// src/routes/AppRoutes.jsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import GrammarCheck from '../pages/GrammarCheck'; // Đảm bảo đường dẫn này đúng với vị trí file GrammarCheck của bạn
import AnalyzeLevel from '../pages/AnalyzeLevel'; // Thêm các trang khác nếu có
import WritingFeedback from '../pages/WritingFeedback';
import Vocabulary from '../pages/Vocabulary';

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<GrammarCheck />} />
      <Route path="/analyze" element={<AnalyzeLevel />} /> {/* Thêm các route cho các trang khác */}
      <Route path="/feedback" element={<WritingFeedback />} />
      <Route path="/vocabulary" element={<Vocabulary />} />
    </Routes>
  );
}

export default AppRoutes;