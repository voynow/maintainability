import React from 'react';
import Login from './components/Login';
import Main from './components/Main';
import Register from './components/Register';
import { useAppContext } from './AppContext';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import ErrorBoundary from './ErrorBoundary';


const App = () => {
    const { isLoggedIn } = useAppContext();

    return (
        <ErrorBoundary>
            <div className="h-screen" style={{ backgroundColor: '#FDF2E9' }}>
                <BrowserRouter>
                    <Routes>
                        <Route path="/login" element={!isLoggedIn ? <Login /> : <Navigate to="/" />} />
                        <Route path="/register" element={!isLoggedIn ? <Register /> : <Navigate to="/" />} />
                        <Route path="*" element={isLoggedIn ? <Main /> : <Navigate to="/login" />} />
                    </Routes>
                </BrowserRouter>
            </div>
        </ErrorBoundary>
    );
};

export default App;
