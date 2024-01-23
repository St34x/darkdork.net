import React, { useEffect, useState} from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Index from './components/views/Index';
import LoginPage from './components/views/LoginPage';
import ChatPage from './components/views/ChatPage';
import ProtectedRoute from './components/views/ProtectedRoute';
import Dashboard from './components/views/Dashboard';

const App = () => {
    const isAuthenticated = true;

    // const isAuthenticated = !!localStorage.getItem('Authenticated');
    
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Index />} />
                <Route path="/login" element={<LoginPage />} />
                <Route 
                    path="/chat" 
                    element={
                        <ProtectedRoute isAuthenticated={isAuthenticated}>
                            <ChatPage />
                        </ProtectedRoute>
                    } 
                />
                <Route 
                    path="/dashboard" 
                    element={
                        <ProtectedRoute isAuthenticated={isAuthenticated}>
                            <Dashboard />
                        </ProtectedRoute>
                    } 
                />

                {/* Other routes */}
            </Routes>
        </Router>
    );
};

export default App;
