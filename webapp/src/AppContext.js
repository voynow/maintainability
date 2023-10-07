import React, { createContext, useContext, useState } from 'react';

const AppContext = createContext();

export const useAppContext = () => {
    return useContext(AppContext);
};

export const AppProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [currentPage, setCurrentPage] = useState('Analytics');

    const value = {
        isLoggedIn,
        setIsLoggedIn,
        currentPage,
        setCurrentPage
    };

    return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
