import { useState } from 'react';
import supabase from '../supabaseClient';
import { useNavigate } from 'react-router-dom';

function Login() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    async function signInWithEmail() {
        const { error } = await supabase.auth.signIn({
            email,
            password,
        });

        if (error) {
            setErrorMessage(error.message || 'An error occurred during sign-in.');
            console.error("Error during sign-in:", error);
        } else {
            navigate('/'); // Navigate to the main page upon successful login
        }
    }

    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-4xl font-bold mb-4">Login</h1>
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mb-2 p-1 border rounded w-64 bg-transparent"
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mb-4 p-1 border rounded w-64 bg-transparent"
            />
            <button
                onClick={signInWithEmail}
                className="px-6 py-2 border rounded text-xl font-medium hover:bg-gray-200 transition duration-300 w-64"
            >
                Sign In
            </button>
            <p onClick={() => navigate('/signup')} className="cursor-pointer text-blue-600 hover:underline mt-4">
                Don't have an account? Sign Up
            </p>
            {errorMessage && <p className="text-red-500 mt-2">{errorMessage}</p>}
        </div>
    );
}

export default Login;
