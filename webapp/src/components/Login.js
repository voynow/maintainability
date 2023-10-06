import React from 'react';

const Login = ({ setIsLoggedIn }) => {
    const handleLogin = () => {
        setIsLoggedIn(true);
    };

    return (
        <div className="flex items-center justify-center h-full">
            <button onClick={handleLogin} className="p-3 w-full bg-green-500 text-white rounded">
                Login
            </button>
        </div>
    );
};
