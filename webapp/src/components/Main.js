import React, { useState } from 'react';
import NavButton from './common/NavButton';
import Analytics from './Analytics';
import APIKeys from './APIKeys';
import Payments from './Payments';
import Profile from './Profile';

const Main = () => {
  const [currentPage, setCurrentPage] = useState('Analytics');

  const renderPage = () => {
    switch (currentPage) {
      case 'Analytics':
        return <Analytics />;
      case 'API Keys':
        return <APIKeys />;
      case 'Payments':
        return <Payments />;
      case 'Profile':
        return <Profile />;
      default:
        return <Analytics />;
    }
  };

  return (
    <div className='flex flex-col h-full p-8 bg-white rounded-lg shadow-md w-full'>
      <nav className='mb-4 flex justify-between items-center'>
        <button onClick={() => setCurrentPage('Analytics')}>
          Home
        </button>
        <div>
          <NavButton label="API Keys" onClick={() => setCurrentPage('API Keys')} />
          <NavButton label="Payments" onClick={() => setCurrentPage('Payments')} />
          <NavButton label="Profile" onClick={() => setCurrentPage('Profile')} />
        </div>
      </nav>
      <div id='content' className='flex flex-col items-center'>
        {renderPage()}
      </div>
    </div>
  );
};

export default Main;
