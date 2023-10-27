import React, { useState, useEffect } from 'react';
import { AppBar, Toolbar, Typography, ButtonBase, Select, MenuItem } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { useAppContext } from '../AppContext';
import Profile from './Profile';
import axios from 'axios';


const Header = () => {
    const [popupOpen, setPopupOpen] = useState(false);
    const [projects, setProjects] = useState([]);
    const { selectedProject, setSelectedProject, email } = useAppContext();

    const togglePopup = () => {
        setPopupOpen(!popupOpen);
    };

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                const response = await axios.get("/get_user_projects", {
                    params: { user_email: email },
                    headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
                });
                if (response.status === 200) {
                    setProjects(response.data);
                }
            } catch (err) {
                setError("An error occurred while fetching projects.");
            }
        };

        fetchProjects();
    }, [email]);

    return (
        <>
            <AppBar position="static" elevation={0} sx={{ zIndex: 1201, backgroundColor: '#FDF2E9' }}>
                <Toolbar>
                    <Typography variant="h5" sx={{ fontWeight: 600, flexGrow: 1, color: '#333333' }}>
                        Maintainability
                    </Typography>
                    <Select value={selectedProject || ''} onChange={(e) => setSelectedProject(e.target.value)}>
                        {projects.map((project, index) => (
                            <MenuItem key={index} value={project.project_name}>{project.project_name}</MenuItem>
                        ))}
                    </Select>
                    <ButtonBase onClick={togglePopup} sx={{ borderRadius: '50%', padding: '12px' }}>
                        <AccountCircleIcon sx={{ marginRight: '6px', fontSize: '35px', color: '#CD5C5C' }} />
                        <Typography variant="body1" sx={{ fontSize: '24px', color: '#333333' }}>
                            {email}
                        </Typography>
                    </ButtonBase>
                </Toolbar>
            </AppBar>
            <Profile open={popupOpen} onClose={togglePopup} />
        </>
    );
};

export default Header;
