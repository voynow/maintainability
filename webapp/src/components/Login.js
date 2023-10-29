import { useState, useEffect } from 'react';

import supabase from '../supabaseClient';
import { useAppContext } from '../AppContext';

function Login() {
    const [user, setUser] = useState(null);
    const { isLoggedIn, setIsLoggedIn } = useAppContext();

    useEffect(() => {
        checkUser();
        window.addEventListener('hashchange', function () {
            checkUser();
        });
    }, [])
    async function checkUser() {
        const user = supabase.auth.user();
        setUser(user);
        setIsLoggedIn(!!user);
    }
    async function signInWithGithub() {
        await supabase.auth.signIn({
            provider: 'github'
        });
    }
    async function signOut() {
        await supabase.auth.signOut();
        setUser(null);
    }
    if (user) {
        return (
            <div className="App">
                <h1>Hello, {user.email}</h1>
                <button onClick={signOut}>Sign out</button>
            </div>
        )
    }
    return (
        <div className="App">
            <h1>Hello, please sign in!</h1>
            <button onClick={signInWithGithub}>Sign In</button>
        </div>
    );
}

export default Login;