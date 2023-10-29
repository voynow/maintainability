import { useState, useEffect } from 'react';
import supabase from '../supabaseClient';
import { useAppContext } from '../AppContext';

function Login() {
    const [user, setUser] = useState(null);
    const { setIsLoggedIn, setEmail: setGlobalEmail } = useAppContext();

    useEffect(() => {
        checkUser();
        window.addEventListener('hashchange', function () {
            checkUser();
        });
    }, []);

    async function checkUser() {
        const user = supabase.auth.user();
        setUser(user);
        setIsLoggedIn(!!user);
        if (user) {
            setGlobalEmail(user.email);
        }
    }

    async function signInWithGithub() {
        await supabase.auth.signIn({
            provider: 'github'
        });
    }

    async function signOut() {
        await supabase.auth.signOut();
        setUser(null);
        setIsLoggedIn(false);
        setGlobalEmail(null);
    }

    return (
        <div className="h-screen bg-gray-100 flex items-center justify-center">
            {user ? (
                <div className="bg-white p-6 rounded-lg shadow-lg w-1/4 text-center">
                    <h1 className="text-2xl font-semibold mb-4">Hello, {user.email}</h1>
                    <button onClick={signOut} className="bg-red-500 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded">
                        Sign out
                    </button>
                </div>
            ) : (
                <div className="bg-white p-6 rounded-lg shadow-lg w-1/4 text-center">
                    <h1 className="text-2xl font-semibold mb-4">Hello, please sign in!</h1>
                    <button onClick={signInWithGithub} className="bg-blue-500 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded">
                        Sign In
                    </button>
                </div>
            )}
        </div>
    );
}

export default Login;
