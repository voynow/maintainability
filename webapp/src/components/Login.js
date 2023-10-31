import { useState, useEffect } from 'react';
import supabase from '../supabaseClient';
import { useAppContext } from '../AppContext';
import { Link } from 'react-router-dom';

function Login() {
    const { setIsLoggedIn, setEmail } = useAppContext();
    const [email, setInputEmail] = useState('');
    const [password, setInputPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        const user = supabase.auth.user();
        setIsLoggedIn(!!user);
        if (user) {
            setEmail(user.email);
        }
    }, []);

    async function signInWithEmail() {
        const { data, error } = await supabase.auth.signIn({
            email,
            password,
        });

        if (error) {
            setErrorMessage(error.message || 'An error occurred during sign-in.');
            console.error("Error during sign-in:", error);
        }
    }

    return (
        <div className="h-screen bg-gray-100 flex items-center justify-center">
            <div className="bg-white p-6 rounded-lg shadow-lg w-1/4 text-center">
                <h1 className="text-2xl font-semibold mb-4">Login</h1>
                <input type="email" placeholder="Email" value={email} onChange={(e) => setInputEmail(e.target.value)} className="mb-2 p-1 border rounded w-full" />
                <input type="password" placeholder="Password" value={password} onChange={(e) => setInputPassword(e.target.value)} className="mb-4 p-1 border rounded w-full" />
                <button onClick={signInWithEmail} className="bg-blue-500 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded mb-2 w-full">Sign In</button>
                <Link to="/signup">Don't have an account? Sign Up</Link>
                {errorMessage && <p className="text-red-500">{errorMessage}</p>}
            </div>
        </div>
    );
}

export default Login;
