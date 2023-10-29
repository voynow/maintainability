import React, { createContext, useContext, useState, useEffect } from 'react';
import supabase from './supabaseClient';

const AppContext = createContext();

export const useAppContext = () => {
    return useContext(AppContext);
};

export const AppProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [email, setEmail] = useState(null);

    useEffect(() => {
        const session = supabase.auth.session();
        setIsLoggedIn(!!session);
        if (session) {
            setEmail(session.user.email);
        }
    }, []);

    const logout = async () => {
        const { error } = await supabase.auth.signOut();
        if (error) {
            console.error("Error during logout:", error);
        } else {
            setIsLoggedIn(false);
            setEmail(null);
        }
    };

    const value = {
        isLoggedIn,
        setIsLoggedIn,
        email,
        setEmail,
        logout
    };

    return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
