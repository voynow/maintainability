import React, { useState } from 'react';
import axios from 'axios';
import { useHistory } from 'react-router-dom';

const Register = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('user');
    const history = useHistory();

    const handleRegister = async () => {
        try {
            await axios.post("/register", {
                email,
                password,
                role
            });
            history.push('/login');
        } catch (err) {
            console.error("Registration failed:", err);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-r from-blue-400 via-blue-500 to-blue-600">
            <div className="p-8 bg-white rounded-lg shadow-md w-1/3 text-center">
                <h1 className="text-2xl mb-4">Register for Maintainability</h1>
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
                    className="mb-2 p-1 border rounded"
                />
                <select
                    onChange={(e) => setRole(e.target.value)}
                    className="mb-4 p-1 border rounded"
                >
                    <option value="user">User</option>
                    <option value="admin">Admin</option>
                </select>
                <button onClick={handleRegister} className="p-3 w-full bg-green-500 text-white rounded">
                    Register
                </button>
            </div>
        </div>
    );
};

export default Register;
