import React, { useState, useEffect } from 'react';
import { useAppContext } from '../AppContext';
import axios from 'axios';
import '../axiosConfig';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';

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
        <Box
            sx={{
                backgroundColor: (theme) => theme.palette.primary.main,
                height: '100vh',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center'
            }}
        >
            <div className="p-8 bg-white rounded-lg shadow-md w-1/3 text-center">
                <h1 className="text-3xl mb-4">Maintainability</h1>
                <TextField
                    type="text"
                    placeholder="Email"
                    onChange={(e) => setEmail(e.target.value)}
                    className="mb-4 p-1 border rounded w-full"
                />
                <TextField
                    type="password"
                    placeholder="Password"
                    onChange={(e) => setPassword(e.target.value)}
                    className="mb-4 p-1 border rounded w-full"
                />
                <Button onClick={handleLogin} className="p-3 w-full bg-green-500 text-white rounded">
                    Login
                </Button>
                <p className="mt-4">
                    New here? <a href="/register" className="text-blue-400 underline">Register</a>
                </p>
                {errorMessage && <p className="text-red-500 mt-2">{errorMessage}</p>}
            </div>
        </Box>
    );
};

export default Login;
