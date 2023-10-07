import React from 'react';
import Login from './components/Login';
import Main from './components/Main';
import { useAppContext } from './AppContext';

const App = () => {
    const { isLoggedIn, setIsLoggedIn } = useAppContext();

    return (
        <div className="h-screen bg-gradient-to-r from-blue-400 via-blue-500 to-blue-600">
            {isLoggedIn ? <Main /> : <Login />}
        </div>
    );
};

export default App;
