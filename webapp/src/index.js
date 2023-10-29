import React from 'react';
import ReactDOM from 'react-dom';
import { AppProvider } from './AppContext';
import App from './App';
import './index.css';
import './axiosConfig';

ReactDOM.render(
    <React.StrictMode>
        <AppProvider>
            <App />
        </AppProvider>
    </React.StrictMode>,
    document.getElementById('root')
);
