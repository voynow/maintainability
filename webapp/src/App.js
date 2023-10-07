import React from 'react';
import Login from './components/Login';
import Main from './components/Main';
import Register from './components/Register';
import { useAppContext } from './AppContext';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';


const App = () => {
    const { isLoggedIn } = useAppContext();

    return (
        <div className="h-screen bg-gradient-to-r from-blue-400 via-blue-500 to-blue-600">
            <BrowserRouter>
                <Routes>
                    <Route path="/login" element={!isLoggedIn ? <Login /> : <Navigate to="/" />} />
                    <Route path="/register" element={!isLoggedIn ? <Register /> : <Navigate to="/" />} />
                    <Route path="*" element={isLoggedIn ? <Main /> : <Navigate to="/login" />} />
                </Routes>
            </BrowserRouter>
        </div>
    );
};

export default App;
