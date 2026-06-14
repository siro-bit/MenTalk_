import React from "react";
import './App.css';
import StudentList from './pages/studentlist'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ReportPage from "./pages/ReportPage";
import ChatPage from "./pages/ChatPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<StudentList />} />
        <Route path="/report" element={<ReportPage />} />
        <Route path="/chat" element={<ChatPage />} />
        
      </Routes>
    </BrowserRouter>
    
  );
}

export default App;




