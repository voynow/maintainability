import React, { useState } from 'react';
import { useAppContext } from '../AppContext';
import axios from 'axios';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';

const APIKeys = () => {
    const [apiKey, setApiKey] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const { email } = useAppContext();

    const generateApiKey = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.post('/generate_key', { email });
            setApiKey(response.data.api_key);
        } catch (err) {
            console.error('Email:', email);
            console.error('Failed to generate API key:', err);
            setError('Failed to generate API key. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = () => {
        navigator.clipboard.writeText(apiKey).catch(err => {
            console.error('Could not copy API key:', err);
        });
    };

    return (
        <div>
            <Button variant="contained" color="primary" onClick={generateApiKey} disabled={loading}>
                {loading ? <CircularProgress size={24} /> : 'Generate API Key'}
            </Button>
            {apiKey && (
                <div>
                    <Typography variant="h6">Your API Key:</Typography>
                    <Typography variant="body1">{apiKey}</Typography>
                    <Button variant="outlined" onClick={copyToClipboard}>Copy to Clipboard</Button>
                </div>
            )}
            {error && <Typography variant="body2" color="error">{error}</Typography>}
        </div>
    );
};

export default APIKeys;
