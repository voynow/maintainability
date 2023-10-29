import { useEffect } from 'react';
import supabase from '../supabaseClient';
import { useAppContext } from '../AppContext';

function Login() {
    const { setIsLoggedIn, setEmail, isLoggedIn } = useAppContext();

    useEffect(() => {
        const user = supabase.auth.user();
        setIsLoggedIn(!!user);
        if (user) {
            setEmail(user.email);
        }
    }, []);

    async function signInWithGithub() {
        await supabase.auth.signIn({
            provider: 'github'
        });
    }

    return (
        <div className="h-screen bg-gray-100 flex items-center justify-center">
            {!isLoggedIn ? (
                <div className="bg-white p-6 rounded-lg shadow-lg w-1/4 text-center">
                    <h1 className="text-2xl font-semibold mb-4">Hello, please sign in!</h1>
                    <button onClick={signInWithGithub} className="bg-blue-500 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded">
                        Sign In
                    </button>
                </div>
            ) : null}
        </div>
    );
}

export default Login;
