import React from 'react';
import { AppBar, Toolbar, Typography, IconButton, ButtonBase } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { useAppContext } from '../AppContext';
import { useNavigate } from 'react-router-dom';

const Header = ({ toggleSidebar }) => {
    const navigate = useNavigate();
    const { email } = useAppContext();

    const goToProfile = () => {
        navigate('/profile');
    };

    return (
        <AppBar position="static" sx={{ zIndex: 1201, backgroundColor: '#3b82f6' }}>
            <Toolbar>
                <IconButton edge="start" color="inherit" aria-label="menu" onClick={toggleSidebar}>
                    <MenuIcon />
                </IconButton>
                <Typography variant="h6" sx={{ fontWeight: 600, flexGrow: 1 }}>
                    Maintainability
                </Typography>
                <ButtonBase onClick={goToProfile} sx={{ borderRadius: '50%' }}>
                    <AccountCircleIcon sx={{ marginRight: '5px', color: '#FFFFFF' }} />
                    <Typography variant="body1" sx={{ color: '#FFFFFF' }}>
                        {email}
                    </Typography>
                </ButtonBase>
            </Toolbar>
        </AppBar>
    );
};

export default Header;
