import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CircularProgress from '@mui/material/CircularProgress';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Button from '@mui/material/Button';
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

    return (
        <div className="space-y-4">
            <Table className="min-w-full bg-white rounded-lg shadow-md">
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
                            <TableCell>
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

            <div className="flex space-x-2 mt-4">
                <TextField
                    type="text"
                    placeholder="New Key Name"
                    value={newKeyName}
                    onChange={(e) => setNewKeyName(e.target.value)}
                    className="p-1 w-full rounded border-2"
                />
                <button
                    onClick={generateApiKey}
                    disabled={loading || !newKeyName}
                    className="bg-blue-500 text-white rounded-lg hover:bg-blue-300 focus:outline-none focus:ring focus:ring-blue-200"
                >
                    {loading ? <CircularProgress size={24} /> : '+'}
                </button>
            </div>
        </div>
    );
};

export default APIKeys;