import React from 'react';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import { Link } from 'react-router-dom';

const Sidebar = () => {
    return (
        <Drawer variant="permanent" anchor="left">
            <List>
                {['Home', 'API Keys', 'Payments', 'Profile'].map((text, index) => (
                    <ListItem key={text}>
                        <Link to={index === 0 ? "/" : `/${text.toLowerCase().replace(' ', '')}`}>
                            <ListItemText primary={text} />
                        </Link>
                    </ListItem>
                ))}
            </List>
        </Drawer>
    );
};

export default Sidebar;
