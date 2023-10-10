import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';

const Header = ({ toggleSidebar }) => {
    return (
        <AppBar position="static" style={{ zIndex: 1201, backgroundColor: '##3b82f6' }}>
            <Toolbar>
                <IconButton edge="start" color="inherit" aria-label="menu" onClick={toggleSidebar}>
                    <MenuIcon />
                </IconButton>
                <Typography variant="h6" style={{ fontWeight: 600 }}>
                    Maintainability
                </Typography>
            </Toolbar>
        </AppBar>
    );
};

export default Header;
