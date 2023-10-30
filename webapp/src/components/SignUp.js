import { useState } from 'react';
import supabase from '../supabaseClient';
import { Link } from 'react-router-dom';

function SignUp() {
    const [email, setInputEmail] = useState('');
    const [password, setInputPassword] = useState('');
    const [emailSent, setEmailSent] = useState(false);

    async function signUpWithEmail() {
        const { data, error } = await supabase.auth.signUp({
            email,
            password,
        });

        if (error) {
            console.error("Error during sign-up:", error);
        } else {
            setEmailSent(true);
        }
    }

    return (
        <div className="h-screen bg-gray-100 flex items-center justify-center">
            <div className="bg-white p-6 rounded-lg shadow-lg w-1/4 text-center">
                {emailSent ? (
                    <p>A verification email has been sent. Please check your inbox.</p>
                ) : (
                    <>
                        <h1 className="text-2xl font-semibold mb-4">Sign Up</h1>
                        <input type="email" placeholder="Email" value={email} onChange={(e) => setInputEmail(e.target.value)} className="mb-2 p-1 border rounded w-full" />
                        <input type="password" placeholder="Password" value={password} onChange={(e) => setInputPassword(e.target.value)} className="mb-4 p-1 border rounded w-full" />
                        <button onClick={signUpWithEmail} className="bg-green-500 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded mb-2 w-full">Sign Up</button>
                        <Link to="/login">Already have an account? Log In</Link>
                    </>
                )}
            </div>
        </div>
    );
}

export default SignUp;
