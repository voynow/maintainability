import { useState, useEffect } from 'react';
import supabase from '../supabaseClient';
import { useAppContext } from '../AppContext';

function Login() {
    const { setIsLoggedIn, setEmail, isLoggedIn } = useAppContext();
    const [email, setInputEmail] = useState('');
    const [password, setInputPassword] = useState('');

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
            console.error("Error during sign-in:", error);
        } else {
            console.log("Signed in:", data);
        }
    }

    return (
        <div className="h-screen bg-gray-100 flex items-center justify-center">
            {!isLoggedIn ? (
                <div className="bg-white p-6 rounded-lg shadow-lg w-1/4 text-center">
                    <h1 className="text-2xl font-semibold mb-4">Hello, please sign in!</h1>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setInputEmail(e.target.value)}
                        className="mb-2 p-1 border rounded"
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setInputPassword(e.target.value)}
                        className="mb-2 p-1 border rounded"
                    />
                    <button onClick={signInWithEmail} className="bg-blue-500 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded">
                        Sign In
                    </button>
                </div>
            ) : null}
        </div>
    );
}

export default Login;
