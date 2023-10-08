import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

const Register = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleRegister = async () => {
        try {
            await axios.post("/register", {
                email,
                password,
                role: "some_default_role"
            });
            navigate('/login');
        } catch (err) {
            console.error("Registration failed:", err);
        }
    };


    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-r from-blue-400 via-blue-500 to-blue-600">
            <div className="p-8 bg-white rounded-lg shadow-md w-1/3 text-center">
                <h1 className="text-3xl mb-4">Welcome to Maintainability!</h1>
                <TextField
                    type="text"
                    placeholder="Email"
                    onChange={(e) => setEmail(e.target.value)}
                    className="mb-2 p-1 border rounded w-full"
                />
                <TextField
                    type="password"
                    placeholder="Password"
                    onChange={(e) => setPassword(e.target.value)}
                    className="mb-4 p-1 border rounded w-full"
                />
                <Button onClick={handleRegister} className="p-3 w-full bg-green-500 text-white rounded">
                    Register
                </Button>
                <p className="mt-4">
                    Already have an account? <a href="/login" className="text-blue-500 underline">Log In</a>
                </p>
            </div>
        </div>
    );
};

export default Register;
