import React, { createContext, useContext, useState, useEffect } from 'react';

const AppContext = createContext();

export const useAppContext = () => {
    return useContext(AppContext);
};

export const AppProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [currentPage, setCurrentPage] = useState('Analytics');
    const [email, setEmail] = useState(null);
    const [selectedProject, setSelectedProject] = useState(null);

    const logout = () => {
        localStorage.removeItem('access_token');
        setIsLoggedIn(false);
    };

    const value = {
        isLoggedIn,
        setIsLoggedIn,
        currentPage,
        setCurrentPage,
        email,
        setEmail,
        logout,
        selectedProject,
        setSelectedProject
    };

    return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
