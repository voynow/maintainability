import React from 'react';
import { Route, Routes } from 'react-router-dom';
import APIKeys from './APIKeys';
import Analytics from './Analytics';
import Footer from './Footer';
import Header from './Header';
import MainContent from './MainContent';
import Payments from './Payments';
import Profile from './Profile';

const Main = () => {



  return (
    <div className='flex flex-col h-full'>
      <Header />
      <div className='flex flex-row flex-grow'>
        <MainContent>
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
