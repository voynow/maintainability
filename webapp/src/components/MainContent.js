import React from 'react';
import Container from '@mui/material/Container';

const MainContent = ({ children }) => {
    return (
        <Container>
            {children}
        </Container>
    );
};

export default MainContent;
