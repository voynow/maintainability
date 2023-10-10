import React from 'react';
import { Link } from 'react-router-dom';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';

const Sidebar = ({ isOpen, toggleDrawer }) => {
    return (
        <Drawer variant="temporary" open={isOpen} onClose={toggleDrawer}>
            <List style={{ paddingTop: '80px' }}>
                {['Home', 'API Keys', 'Payments', 'Profile'].map((text, index) => (
                    <ListItem
                        key={text}
                        component={Link}
                        to={index === 0 ? "/" : `/${text.toLowerCase().replace(' ', '')}`}
                        onClick={toggleDrawer}
                    >
                        <ListItemText primary={text} />
                    </ListItem>
                ))}
            </List>
        </Drawer>
    );
};

export default Sidebar;
