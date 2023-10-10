import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';
import { useAppContext } from '../AppContext';

const APIKeys = () => {
    const [apiKeys, setApiKeys] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const { email } = useAppContext();

    useEffect(() => {
        const fetchApiKeys = async () => {
            try {
                const response = await axios.get('/api_keys', { params: { email } });
                setApiKeys(response.data.api_keys);
            } catch (err) {
                setError('Failed to fetch API keys.');
            }
        };
        fetchApiKeys();
    }, []);

    const generateApiKey = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.post('/generate_key', { email });
            setApiKeys([...apiKeys, response.data]);
        } catch (err) {
            setError('Failed to generate API key.');
        } finally {
            setLoading(false);
        }
    };

    const deleteApiKey = async (apiKey) => {
        try {
            await axios.delete(`/api_keys/${apiKey}`);
            setApiKeys(apiKeys.filter(key => key.api_key !== apiKey));
        } catch (err) {
            setError('Failed to delete API key.');
        }
    };

    const copyToClipboard = (apiKey) => {
        navigator.clipboard.writeText(apiKey).catch(err => {
            setError('Failed to copy API key.');
        });
    };

    return (
        <div className="space-y-4">
            <Button
                variant="contained"
                color="primary"
                onClick={generateApiKey}
                disabled={loading}
            >
                {loading ? <CircularProgress size={24} /> : 'Generate New Key'}
            </Button>
            {apiKeys.map((keyObj, index) => (
                <div key={index} className="flex justify-between items-center">
                    <Typography variant="body1">{keyObj.api_key}</Typography>
                    <div className="space-x-2">
                        <Button variant="outlined" onClick={() => deleteApiKey(keyObj.api_key)}>Delete</Button>
                        <Button variant="outlined" onClick={() => copyToClipboard(keyObj.api_key)}>Copy</Button>
                    </div>
                </div>
            ))}
            {error && <Typography variant="body2" color="error">{error}</Typography>}
        </div>
    );
};

export default APIKeys;
