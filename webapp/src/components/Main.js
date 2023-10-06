import React, { useState } from 'react';
import Analytics from './Analytics';
import APIKeys from './APIKeys';
import Payments from './Payments';
import Profile from './Profile';

const Main = () => {
    const [currentTab, setCurrentTab] = useState('Analytics');

    const renderContent = () => {
        switch (currentTab) {
            case 'Analytics': return <Analytics />;
            case 'APIKeys': return <APIKeys />;
            case 'Payments': return <Payments />;
            case 'Profile': return <Profile />;
            default: return <Analytics />;
        }
    };

    return (
        <div className="flex flex-col h-full p-8 bg-white rounded-lg shadow-md">
            <nav className="mb-4 flex justify-end">
                <button onClick={() => setCurrentTab('Analytics')} className="mr-4">Analytics</button>
                <button onClick={() => setCurrentTab('APIKeys')} className="mr-4">API Keys</button>
                <button onClick={() => setCurrentTab('Payments')} className="mr-4">Payments</button>
                <button onClick={() => setCurrentTab('Profile')}>Profile</button>
            </nav>
            {renderContent()}
        </div>
    );
};

export default Main;