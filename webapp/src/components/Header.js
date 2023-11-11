import React, { useState, useEffect } from 'react';
import { AppBar, Toolbar, Typography, ButtonBase, IconButton } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import DashboardIcon from '@mui/icons-material/Dashboard';
import { useAppContext } from '../AppContext';
import Profile from './Profile';
import ProjectsDashboard from './ProjectsDashboard';
import api from '../axiosConfig';


const Header = () => {
    const [popupOpen, setPopupOpen] = useState(false);
    const { selectedProject, setSelectedProject, email, isFetchingProjects, setIsFetchingProjects, projects, setProjects } = useAppContext();
    const [error, setError] = useState(null);
    const [dashboardOpen, setDashboardOpen] = useState(false);


    const togglePopup = () => {
        setPopupOpen(!popupOpen);
    };

    useEffect(() => {
        let isMounted = true;
        const fetchProjects = async () => {
            setIsFetchingProjects(true);
            try {
                const response = await api.get("/get_user_projects", {
                    params: { user_email: email },
                });
                if (isMounted && response.status === 200) {
                    setProjects(response.data);
                    if (!selectedProject && response.data.length > 0) {
                        setSelectedProject(response.data[0].project_name);
                    }
                }
            } catch (err) {
                if (isMounted) {
                    setError("An error occurred while fetching projects.");
                }
            } finally {
                if (isMounted) {
                    setIsFetchingProjects(false);
                }
            }
        };

        fetchProjects();

        return () => {
            // Set the flag to false when the component unmounts
            isMounted = false;
        };
    }, [email, selectedProject, setSelectedProject]);


    return (
        <>
            <AppBar position="static" elevation={0} sx={{ zIndex: 1201, backgroundColor: '#FDF2E9' }}>
                <Toolbar>
                    <Typography variant="h5" sx={{ fontWeight: 600, flexGrow: 1, color: '#333333' }}>
                        Maintainability
                    </Typography>

                    {projects.length ? (
                        <IconButton onClick={() => setDashboardOpen(true)} sx={{ marginRight: 2 }}>
                            <DashboardIcon sx={{ color: '#333333' }} />
                        </IconButton>
                    ) : (
                        <Typography variant="body1" sx={{ marginRight: 2, color: '#aaaaaa' }}>
                            No projects found
                        </Typography>
                    )}

                    <IconButton onClick={togglePopup} sx={{ borderRadius: '50%', padding: '12px' }}>
                        <AccountCircleIcon sx={{ marginRight: '6px', fontSize: '35px', color: '#CD5C5C' }} />
                        <Typography variant="body1" sx={{ fontSize: '20px', color: '#333333' }}>
                            {email}
                        </Typography>
                    </IconButton>
                </Toolbar>
            </AppBar>

            <Profile open={popupOpen} onClose={togglePopup} />
            <ProjectsDashboard open={dashboardOpen} onClose={() => setDashboardOpen(false)} />
        </>
    );
};

export default Header;