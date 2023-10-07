import React, { useState, useEffect } from 'react';
import { useAppContext } from '../AppContext';
import axios from 'axios';
import '../axiosConfig';

const Login = () => {
    const { setIsLoggedIn } = useAppContext();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [mounted, setMounted] = useState(true);

    useEffect(() => {
        setMounted(true);
        return () => setMounted(false);
    }, []);

    const handleLogin = async () => {
        try {
            const response = await axios.post("/token", {
                email,
                password,
            });
            if (mounted) {
                const { access_token } = response.data;
                localStorage.setItem("access_token", access_token);
                setIsLoggedIn(true);
                setErrorMessage('');
            }
        } catch (err) {
            if (mounted) {
                const errMsg = err.response?.data?.detail || 'Login failed';
                console.error(`Login failed: ${errMsg}, status code: ${err.response?.status}`);
                setErrorMessage(errMsg);
            }
        }
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-r from-blue-400 via-blue-500 to-blue-600">
            <div className="p-8 bg-white rounded-lg shadow-md w-1/3 text-center">
                <h1 className="text-4xl mb-4">Maintainability</h1>
                <input
                    type="text"
                    placeholder="Email"
                    onChange={(e) => setEmail(e.target.value)}
                    className="mb-2 p-1 border rounded"
                />
                <input
                    type="password"
                    placeholder="Password"
                    onChange={(e) => setPassword(e.target.value)}
                    className="mb-4 p-1 border rounded"
                />
                <button onClick={handleLogin} className="p-3 w-full bg-green-500 text-white rounded">
                    Login
                </button>
                <p className="mt-4">
                    New here? <a href="/register" className="text-blue-400 underline">Register</a>
                </p>
                {errorMessage && <p className="text-red-500 mt-2">{errorMessage}</p>}
            </div>
        </div>
    );
};

export default Login;
