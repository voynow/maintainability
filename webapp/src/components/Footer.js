import React from 'react';
import Typography from '@mui/material/Typography';

const Footer = () => {
    return (
        <Typography variant="body2" color="textSecondary" align="center">
            {'Copyright © '}
            Maintainability {' '}
            {new Date().getFullYear()}
        </Typography>
    );
};

export default Footer;
