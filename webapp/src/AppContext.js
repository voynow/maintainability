import React, { createContext, useContext, useState, useEffect } from 'react';

const AppContext = createContext();

export const useAppContext = () => {
    return useContext(AppContext);
};

export const AppProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [currentPage, setCurrentPage] = useState('Analytics');
    const [accessToken, setAccessToken] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        if (token) {
            setAccessToken(token);
        }
    }, []);

    const value = {
        isLoggedIn,
        setIsLoggedIn,
        currentPage,
        setCurrentPage,
        accessToken,
        setAccessToken,
    };

    return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
