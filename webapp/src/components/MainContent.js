import React from 'react';

const MainContent = ({ children }) => {
    return (
        <div style={{ flex: 1, padding: '0 16px', marginTop: '64px' }}>
            {children}
        </div>
    );
};

export default MainContent;
