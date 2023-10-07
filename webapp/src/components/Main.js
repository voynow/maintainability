import React from 'react';
import { Route, Routes, Link } from 'react-router-dom';
import Analytics from './Analytics';
import APIKeys from './APIKeys';
import Payments from './Payments';
import Profile from './Profile';
import Register from './Register';

const Main = () => {
  return (
    <div className='flex flex-col h-full p-8 bg-white rounded-lg shadow-md w-full'>
      <nav className='mb-4 flex justify-between items-center'>
        <Link to="/">Home</Link>
        <div>
          <Link to="/apikeys">API Keys</Link>
          <Link to="/payments">Payments</Link>
          <Link to="/profile">Profile</Link>
        </div>
      </nav>
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
  );
};

export default Main;
