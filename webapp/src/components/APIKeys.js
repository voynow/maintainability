import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';
import { useAppContext } from '../AppContext';

const APIKeys = () => {
    const [apiKey, setApiKey] = useState(null);
    const [apiKeys, setApiKeys] = useState([]); // new state
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const { email } = useAppContext();

    useEffect(() => {
        const fetchApiKeys = async () => {
            try {
                const response = await axios.get('/api_keys', { params: { email } });
                setApiKeys(response.data.api_keys);
            } catch (err) {
                console.error('Failed to fetch API keys:', err);
            }
        };

        fetchApiKeys();
    }, []);

    const generateApiKey = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.post('/generate_key', { email });
            setApiKey(response.data.api_key);
            setApiKeys([...apiKeys, response.data.api_key]); // update the list
        } catch (err) {
            setError('Failed to generate API key. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const deleteApiKey = async (keyToDelete) => {
        try {
            await axios.delete(`/api_keys/${keyToDelete}`);
            setApiKeys(apiKeys.filter(key => key !== keyToDelete)); // update the list
        } catch (err) {
            console.error('Failed to delete API key:', err);
        }
    };

    return (
        <div>
            <Button variant="contained" color="primary" onClick={generateApiKey} disabled={loading}>
                {loading ? <CircularProgress size={24} /> : 'Generate API Key'}
            </Button>
            {apiKeys.map((keyObj, index) => (
                <div key={index}>
                    <Typography variant="body1">{keyObj.api_key}</Typography>
                    <Button variant="outlined" onClick={() => deleteApiKey(keyObj.api_key)}>Delete</Button>
                </div>
            ))}
            {error && <Typography variant="body2" color="error">{error}</Typography>}
        </div>
    );
};

export default APIKeys;
