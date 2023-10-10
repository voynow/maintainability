import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { useAppContext } from '../AppContext';

const APIKeys = () => {
    const [apiKeys, setApiKeys] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const { email } = useAppContext();
    const [newKeyName, setNewKeyName] = useState('');
    const [revealKey, setRevealKey] = useState(null);

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
        try {
            const response = await axios.post('/generate_key', { email, name: newKeyName });
            const newKey = { ...response.data, name: newKeyName };
            setApiKeys([...apiKeys, newKey]);
            setNewKeyName('');
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
            <div className="flex space-x-2">
                <input
                    type="text"
                    placeholder="API Key Name"
                    value={newKeyName}
                    onChange={(e) => setNewKeyName(e.target.value)}
                    className="border p-2 rounded"
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={generateApiKey}
                    disabled={loading || !newKeyName}
                >
                    {loading ? <CircularProgress size={24} /> : 'Generate New Key'}
                </Button>
            </div>

            <Table style={{ width: '100%', tableLayout: 'fixed' }}>
                <TableHead>
                    <TableRow>
                        <TableCell style={{ width: '5%' }}>#</TableCell>
                        <TableCell style={{ width: '25%' }}>Name</TableCell>
                        <TableCell style={{ width: '40%' }}>API Key</TableCell>
                        <TableCell style={{ width: '30%' }}>Actions</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {apiKeys.map((keyObj, index) => (
                        <TableRow key={index}>
                            <TableCell>{index + 1}</TableCell>
                            <TableCell>{keyObj.name}</TableCell>
                            <TableCell style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                {revealKey === keyObj.api_key ? keyObj.api_key : '****************'}
                            </TableCell>
                            <TableCell>
                                <Button variant="outlined" onClick={() => deleteApiKey(keyObj.api_key)}>Delete</Button>
                                <Button variant="outlined" onClick={() => copyToClipboard(keyObj.api_key)}>Copy</Button>
                                <Button variant="outlined" onClick={() => setRevealKey(revealKey === keyObj.api_key ? null : keyObj.api_key)}>
                                    {revealKey === keyObj.api_key ? 'Hide' : 'Show'}
                                </Button>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>


            {error && <Typography variant="body2" color="error">{error}</Typography>}
        </div>
    );
};

export default APIKeys;
