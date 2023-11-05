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
                <>
                    <h1 className="text-4xl font-bold mb-4">Sign Up</h1>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="mb-4 p-2 border-2 rounded w-64 bg-transparent"
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="mb-4 p-2 border-2 rounded w-64 bg-transparent"
                    />
                    <button
                        onClick={signUpWithEmail}
                        className="px-6 py-2 border-2 rounded text-xl font-medium hover:bg-gray-200 transition duration-300 w-64"
                    >
                        Sign Up
                    </button>
                    <p onClick={() => navigate('/login')} className="cursor-pointer text-blue-600 hover:underline mt-4">
                        Already have an account? Log In
                    </p>
                    {errorMessage && <p className="text-red-500 mt-2">{errorMessage}</p>}
                </>
            )}
        </div>
    );
}

export default SignUp;
