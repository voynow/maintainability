import React, { useState } from 'react';
import { AppBar, Toolbar, Typography, ButtonBase } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { useAppContext } from '../AppContext';
import Profile from './Profile';
import ProjectsDashboard from './ProjectsDashboard';

const Header = () => {
    const { email } = useAppContext();
    const [popupOpen, setPopupOpen] = useState(false);
    const [dashboardOpen, setDashboardOpen] = useState(false);

    const togglePopup = () => setPopupOpen(!popupOpen);
    const toggleDashboard = () => setDashboardOpen(!dashboardOpen);

    return (
        <>
            <AppBar position="static" elevation={0} sx={{ zIndex: 1201, backgroundColor: '#FDF2E9' }}>
                <Toolbar>
                    <Typography variant="h5" sx={{ fontWeight: 600, flexGrow: 1, color: '#333333' }}>
                        Maintainability
                    </Typography>
                    <ButtonBase onClick={toggleDashboard}>
                        Select Project
                    </ButtonBase>
                    <ButtonBase onClick={togglePopup} sx={{ borderRadius: '50%', padding: '12px' }}>
                        <AccountCircleIcon sx={{ marginRight: '6px', fontSize: '35x', color: '#CD5C5C' }} />
                        <Typography variant="body1" sx={{ fontSize: '20px', color: '#333333' }}>
                            {email}
                        </Typography>
                    </ButtonBase>
                </Toolbar>
            </AppBar>
            <ProjectsDashboard open={dashboardOpen} onClose={toggleDashboard} />
            <Profile open={popupOpen} onClose={togglePopup} />
        </>
    );
};

export default Header;
