import React from 'react';
import ReactDOM from 'react-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { AppProvider } from './AppContext';
import App from './App';

const theme = createTheme({
    palette: {
        primary: {
            main: '#5687C1',
        },
    },
});

ReactDOM.render(
    <React.StrictMode>
        <ThemeProvider theme={theme}>
            <AppProvider>
                <App />
            </AppProvider>
        </ThemeProvider>
    </React.StrictMode>,
    document.getElementById('root')
);
