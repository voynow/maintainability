import React, { useState, useEffect } from 'react';
import { useAppContext } from '../AppContext';
import axios from 'axios';
import '../axiosConfig';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

const Login = () => {
    const { setIsLoggedIn, setEmail: setGlobalEmail } = useAppContext();
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
                setGlobalEmail(email);
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
        <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-t from-gray-100 via-gray-100 to-gray-300">
            <div className="p-8 bg-white rounded-lg shadow-md w-1/3 text-center">
                <h1 className="text-4xl mb-4 font-semibold text-gray-800">Maintainability</h1>
                <TextField
                    type="text"
                    placeholder="Email"
                    onChange={(e) => setEmail(e.target.value)}
                    className="mb-4 p-1 w-full rounded border-2"
                />
                <TextField
                    type="password"
                    placeholder="Password"
                    onChange={(e) => setPassword(e.target.value)}
                    className="mb-4 p-1 w-full rounded border-2"
                />
                <button
                    onClick={handleLogin}
                    className="p-3 w-full bg-blue-300 text-white rounded-lg hover:bg-blue-300 focus:outline-none focus:ring focus:ring-blue-200">
                    Login
                </button>
                <p className="mt-4">
                    New here?&nbsp;
                    <a href="/register" className="text-indigo-400 underline hover:text-indigo-500">Register</a>
                </p>
                {errorMessage && <p className="text-red-500 mt-2">{errorMessage}</p>}
            </div>
        </div>
    );
};


export default Login;
