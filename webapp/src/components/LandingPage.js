// webapp/src/components/LandingPage.js

import React from 'react';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
    let navigate = useNavigate();

    const navigateToLogin = () => {
        navigate('/login');
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-4xl font-bold mb-4">Welcome to Maintainability</h1>
            <button
                onClick={navigateToLogin}
                className="px-6 py-2 border rounded text-xl font-medium hover:bg-gray-200 transition duration-300"
            >
                Log In
            </button>
        </div>
    );
};

export default LandingPage;
