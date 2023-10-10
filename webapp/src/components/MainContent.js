import React from 'react';
import Container from '@mui/material/Container';

const MainContent = ({ children }) => {
    return (
        <Container style={{ flex: 1, overflowY: 'auto', marginTop: '64px' }}>
            {children}
        </Container>
    );
};

export default MainContent;
