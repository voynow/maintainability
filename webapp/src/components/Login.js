import { useAppContext } from '../AppContext';
import axios from 'axios';

const Login = () => {
    const { setIsLoggedIn } = useAppContext();

    const handleLogin = async () => {
        const response = await fetch("/token", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: "yourEmail", password: "yourPassword" })
        });
        const data = await response.json();
        localStorage.setItem("access_token", data.access_token);
        setIsLoggedIn(true);
    };


    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-r from-blue-400 via-blue-500 to-blue-600">
            <div className="p-8 bg-white rounded-lg shadow-md w-1/3 text-center">
                <h1 className="text-2xl mb-4">Welcome to Maintainability</h1>
                <p className="mb-4">Sign in to continue.</p>
                <button onClick={handleLogin} className="p-3 w-full bg-green-500 text-white rounded">
                    Login
                </button>
            </div>
        </div>
    );
};

export default Login;
