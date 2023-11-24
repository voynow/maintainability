import React, { useState, useEffect } from 'react';
import { AppBar, Toolbar, Typography, IconButton, Tooltip } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import AssessmentIcon from '@mui/icons-material/Assessment';
import { useAppContext } from '../AppContext';
import Profile from './Profile';
import ProjectsDashboard from './ProjectsDashboard';
import { Box } from '@mui/system';
import Button from '@mui/material/Button';

const Header = () => {
    const [popupOpen, setPopupOpen] = useState(false);
    const { selectedProject, setSelectedProject } = useAppContext();
    const { isDashboardOpen, toggleDashboardOpen } = useAppContext();


    const togglePopup = () => {
        setPopupOpen(!popupOpen);
    };

    const handleProjectClick = () => {
        // Logic to open project details or summary
    };

    const selectedProjectStyle = {
        fontWeight: 600,
        fontSize: '18px',
        marginRight: '16px',
        color: '#4A4A4A',
        cursor: 'pointer',
        '&:hover': {
            textDecoration: 'underline',
            color: '#333'
        }
    };

    const projectLabelStyle = {
        color: '#CEC7C1',
        marginRight: '4px',
        fontSize: '18px',
        fontWeight: 400,
    };

    const buttonStyle = {
        margin: '0 10px',
        padding: '5px 10px',
        borderRadius: '20px',
        backgroundColor: '#EDE4DC',
        '&:hover': {
            backgroundColor: '#FDF2E9',
            boxShadow: '0px 2px 5px rgba(0, 0, 0, 0.2)'
        },
        color: '#333',
        textTransform: 'none'
    };

    return (
        <>
            <AppBar position="static" elevation={0} sx={{ zIndex: 1201, backgroundColor: '#FDF2E9' }}>
                <Toolbar sx={{ justifyContent: 'space-between' }}>
                    <Typography variant="h6" sx={{ fontWeight: 600, color: '#333' }}>
                        Maintainability
                    </Typography>

                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Typography variant="caption" sx={projectLabelStyle}>
                            Current Project:
                        </Typography>
                        <Typography
                            variant="subtitle1"
                            sx={selectedProjectStyle}
                            onClick={handleProjectClick}
                            title="Click for project details"
                        >
                            {selectedProject || 'No projects found'}
                        </Typography>

                        <Button sx={buttonStyle} onClick={toggleDashboardOpen}>
                            <AssessmentIcon sx={{ marginRight: '5px', color: '#CD5C5C' }} />
                            My Projects
                        </Button>

                        <Button sx={buttonStyle} onClick={togglePopup}>
                            <AccountCircleIcon sx={{ marginRight: '5px', color: '#CD5C5C' }} />
                            My Profile
                        </Button>
                    </Box>
                </Toolbar>
            </AppBar >

            <Profile open={popupOpen} onClose={togglePopup} />
            <ProjectsDashboard open={isDashboardOpen} onClose={toggleDashboardOpen} />
        </>
    );
};

export default Header;