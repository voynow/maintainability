import React from 'react';
import Container from '@mui/material/Container';

const MainContent = ({ children }) => {
    return (
        <div style={{ flex: 1, padding: '0 16px', marginTop: '64px' }}>
            {children}
        </div>
    );
};

export default MainContent;
