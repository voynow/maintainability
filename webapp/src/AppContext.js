import React, { createContext, useContext, useState, useEffect } from 'react';

const AppContext = createContext();

export const useAppContext = () => {
    return useContext(AppContext);
};

export const AppProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [currentPage, setCurrentPage] = useState('Analytics');
    const [email, setEmail] = useState(null);

    const value = {
        isLoggedIn,
        setIsLoggedIn,
        currentPage,
        setCurrentPage,
        email,
        setEmail,
    };

    return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
