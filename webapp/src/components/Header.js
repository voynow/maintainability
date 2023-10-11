import React, { useState } from 'react';
import { AppBar, Toolbar, Typography, IconButton, ButtonBase } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { useAppContext } from '../AppContext';
import Profile from './Profile';
import { Link } from 'react-router-dom';
import { Box } from '@mui/material';

const Header = ({ toggleSidebar }) => {
    const [popupOpen, setPopupOpen] = useState(false);
    const { email } = useAppContext();

    const togglePopup = () => {
        setPopupOpen(!popupOpen);
    };

    return (
        <>
            <AppBar position="static" elevation={0} sx={{ zIndex: 1201, backgroundColor: '#FDF2E9' }}>
                <Toolbar>
                    <Box display="flex" alignItems="center">
                        <IconButton edge="start" color="inherit" aria-label="menu" onClick={toggleSidebar} sx={{ color: '#333333' }}>
                            <MenuIcon />
                        </IconButton>
                    </Box>
                    <Typography variant="h6" sx={{ fontWeight: 600, flexGrow: 1, color: '#333333' }}>
                        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                            Maintainability
                        </Link>
                    </Typography>
                    <ButtonBase onClick={togglePopup} sx={{ borderRadius: '50%', padding: '12px' }}>
                        <AccountCircleIcon sx={{ marginRight: '4px', fontSize: '30px', color: '#CD5C5C' }} />
                        <Typography variant="body1" sx={{ fontSize: '18px', color: '#333333' }}>
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
