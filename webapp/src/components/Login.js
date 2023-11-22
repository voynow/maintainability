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
            navigate('/');
        }
    }

    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <div className="rounded-lg p-8 shadow-2xl bg-white w-96">
                <h1 className="text-4xl font-bold mb-8">Login</h1>
                <div className="mb-4 relative">
                    <span className="absolute inset-y-0 left-0 flex items-center pl-2">
                        <svg className="h-5 w-5 text-gray-500" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                            <path d="M16 17l-4 4m0 0l-4-4m4 4V3"></path>
                        </svg>
                    </span>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="pl-10 pr-3 py-2 border rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                    />
                </div>
                <div className="mb-6 relative">
                    <span className="absolute inset-y-0 left-0 flex items-center pl-2">
                        <svg className="h-5 w-5 text-gray-500" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                            <path d="M19 9l-7 7-7-7"></path>
                        </svg>
                    </span>
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="pl-10 pr-3 py-2 border rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                    />
                </div>
                <button
                    onClick={signInWithEmail}
                    className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50 transition duration-300"
                >
                    Sign In
                </button>
                <p
                    onClick={() => navigate('/signup')}
                    className="text-center text-blue-600 hover:underline mt-4 cursor-pointer"
                >
                    Don't have an account? Sign Up
                </p>
                {errorMessage && <p className="text-red-500 mt-2">{errorMessage}</p>}
            </div>
        </div>
    );
}

export default Login;
