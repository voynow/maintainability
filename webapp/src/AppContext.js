import React, { createContext, useContext, useState, useEffect } from 'react';
import supabase from './supabaseClient';

const AppContext = createContext();

export const useAppContext = () => {
    return useContext(AppContext);
};

export const AppProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [email, setEmail] = useState(null);
    const [projects, setProjects] = useState([]);
    const [selectedProject, setSelectedProject] = useState(null);
    const [isFetchingProjects, setIsFetchingProjects] = useState(true);
    const [isDashboardOpen, setIsDashboardOpen] = useState(false);

    useEffect(() => {
        const session = supabase.auth.session();
        setIsLoggedIn(!!session);
        if (session) {
            setEmail(session.user.email);
        }

        // Listen for changes to authentication state
        const { data: authListener } = supabase.auth.onAuthStateChange((event, session) => {
            // Explicitly set state upon successful login
            if (event === 'SIGNED_IN') {
                setIsLoggedIn(true);
                setEmail(session.user.email);
            }
        });

        return () => {
            authListener.unsubscribe();
        };
    }, []);

    const logout = async () => {
        const { error } = await supabase.auth.signOut();
        if (error) {
            console.error("Error during logout:", error);
        } else {
            setIsLoggedIn(false);
            setEmail(null);
            setProjects([]);
            setSelectedProject(null);
            setIsFetchingProjects(true);
            setIsDashboardOpen(false);
        }
    };

    const toggleDashboardOpen = () => setIsDashboardOpen(!isDashboardOpen);

    const value = {
        isLoggedIn,
        setIsLoggedIn,
        email,
        setEmail,
        logout,
        selectedProject,
        setSelectedProject,
        isFetchingProjects,
        setIsFetchingProjects,
        projects,
        setProjects,
        isDashboardOpen,
        toggleDashboardOpen
    };

    return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
