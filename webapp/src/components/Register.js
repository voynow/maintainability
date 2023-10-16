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
        <div className="flex flex-col items-center justify-center h-screen" style={{ background: 'linear-gradient(to top, #FDF2E9, #EDE4DC)' }}>
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
                <button
                    onClick={handleRegister}
                    className="p-3 w-full text-white border rounded border-2"
                    style={{
                        backgroundColor: 'var(--custom-red)',
                        borderColor: 'var(--custom-red)',
                    }}
                >
                    Register
                </button>
                <p className="mt-4">
                    Already have an account? <a href="/login" className="text-blue-400 underline hover:text-blue-500">Log In</a>
                </p>
            </div>
        </div>
    );
};

export default Register;
