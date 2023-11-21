import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Analytics from './Analytics';
import Footer from './Footer';
import Header from './Header';
import MainContent from './MainContent';

const Main = () => {
  return (
    <div className='flex flex-col min-h-screen'>
      <Header />
      <div className='flex flex-row flex-grow overflow-x-hidden'>
        <MainContent className="max-w-full">
          <Routes>
            <Route index element={<Analytics />} />
          </Routes>
        </MainContent>
      </div>
      <Footer />
    </div>
  );
};

export default Main;
