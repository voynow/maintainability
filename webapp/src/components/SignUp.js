import { useState } from 'react';
import supabase from '../supabaseClient';
import { useNavigate } from 'react-router-dom';

function SignUp() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [emailSent, setEmailSent] = useState(false);

    async function signUpWithEmail() {
        const { error } = await supabase.auth.signUp({
            email,
            password,
        });

        if (error) {
            setErrorMessage(error.message || 'An error occurred during sign-up.');
            console.error("Error during sign-up:", error);
        } else {
            setEmailSent(true);
        }
    }

    return (
        <div className="flex flex-col items-center justify-center h-screen">
            {emailSent ? (
                <p className="text-center">A verification email has been sent. Please check your inbox.</p>
            ) : (
                <div className="rounded-lg p-8 shadow-2xl bg-white w-96">
                    <h1 className="text-4xl font-bold mb-8">Sign Up</h1>
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
                        onClick={signUpWithEmail}
                        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50 transition duration-300"
                    >
                        Sign Up
                    </button>
                    <p
                        onClick={() => navigate('/login')}
                        className="text-center text-blue-600 hover:underline mt-4 cursor-pointer"
                    >
                        Already have an account? Log In
                    </p>
                    {errorMessage && <p className="text-red-500 mt-2">{errorMessage}</p>}
                </div>
            )}
        </div>
    );
}

export default SignUp;

