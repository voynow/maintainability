import React from 'react';
import Login from './components/Login';
import SignUp from './components/SignUp';
import Main from './components/Main';
import LandingPage from './components/LandingPage';
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
                        <Route path="/signup" element={!isLoggedIn ? <SignUp /> : <Navigate to="/" />} />
                        <Route path="/welcome" element={!isLoggedIn ? <LandingPage /> : <Navigate to="/" />} />
                        <Route path="*" element={isLoggedIn ? <Main /> : <Navigate to="/welcome" />} />
                    </Routes>
                </BrowserRouter>
            </div>
        </ErrorBoundary>
    );
};

export default App;