import React, { useState } from 'react';
import Login from './components/Login';
import Main from './components/Main';

const App = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    return (
        <div className="h-screen bg-gradient-to-r from-blue-400 via-blue-500 to-blue-600">
            {isLoggedIn ? <Main /> : <Login setIsLoggedIn={setIsLoggedIn} />}
        </div>
    );
};

export default App;
