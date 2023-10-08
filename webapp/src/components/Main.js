import React from 'react';
import { Route, Routes, Link } from 'react-router-dom';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Analytics from './Analytics';
import APIKeys from './APIKeys';
import Payments from './Payments';
import Profile from './Profile';
import Register from './Register';

const Main = () => {
  return (
    <div className='flex flex-row h-full'>
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
      <div className='flex flex-col h-full p-8 bg-white rounded-lg shadow-md w-full'>
        <div id='content' className='flex flex-col items-center'>
          <Routes>
            <Route index element={<Analytics />} />
            <Route path="/register" element={<Register />} />
            <Route path="/apikeys" element={<APIKeys />} />
            <Route path="/payments" element={<Payments />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </div>
      </div>
    </div>
  );
};

export default Main;
