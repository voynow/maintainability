import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { CircularProgress, TextField, Button, Dialog, DialogActions, DialogContent, DialogTitle, IconButton, Table, TableBody, TableCell, TableHead, TableRow, Typography } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import VisibilityIcon from '@mui/icons-material/Visibility';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { useAppContext } from '../AppContext';

const DeleteDialog = ({ open, onClose, onDelete }) => (
    <Dialog open={open} onClose={onClose}>
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogActions>
            <Button onClick={onClose} color="primary">Cancel</Button>
            <Button onClick={onDelete} color="primary">Delete</Button>
        </DialogActions>
    </Dialog>
);

const APIKeys = () => {
    const [apiKeys, setApiKeys] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [newKeyName, setNewKeyName] = useState('');
    const [revealKey, setRevealKey] = useState(null);
    const [copied, setCopied] = useState(null);
    const [confirmDelete, setConfirmDelete] = useState(null);
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
        try {
            const response = await axios.post('/generate_key', { email, name: newKeyName });
            const newKey = { ...response.data, name: newKeyName };
            setApiKeys([...apiKeys, newKey]);
            setNewKeyName('');
            setDialogOpen(false);
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

    const showAndCopy = (apiKey) => {
        setRevealKey(apiKey);
        navigator.clipboard.writeText(apiKey)
            .then(() => setCopied(apiKey))
            .catch(err => setError('Failed to copy API key.'));
    };

    return (
        <div className="space-y-4">
            <Table className="min-w-full bg-white rounded-lg shadow-md">
                <TableHead>
                    <TableRow style={{ backgroundColor: '#EDE4DC' }}>
                        <TableCell style={{ width: '5%' }}>#</TableCell>
                        <TableCell style={{ width: '25%' }}>Name</TableCell>
                        <TableCell style={{ width: '50%' }}>API Key</TableCell>
                        <TableCell style={{ width: '5%' }}></TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {apiKeys.map((keyObj, index) => (
                        <TableRow key={index} style={{ backgroundColor: '#FDF2E9' }}>
                            <TableCell>{index + 1}</TableCell>
                            <TableCell>{keyObj.name}</TableCell>
                            <TableCell>
                                <div className="flex items-center">
                                    <span>
                                        {revealKey === keyObj.api_key ? keyObj.api_key : '****************'}
                                    </span>
                                    <IconButton onClick={() => showAndCopy(keyObj.api_key)}>
                                        {copied === keyObj.api_key ? <CheckCircleIcon fontSize="small" /> : <VisibilityIcon fontSize="small" />}
                                    </IconButton>
                                </div>
                            </TableCell>
                            <TableCell>
                                <IconButton onClick={() => setConfirmDelete(keyObj.api_key)} color="default">
                                    <DeleteIcon fontSize="small" />
                                </IconButton>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>

            {error && <Typography variant="body2" color="error">{error}</Typography>}

            <Button onClick={() => setDialogOpen(true)} startIcon={<AddIcon />} className="mt-4">
                Add API Key
            </Button>

            <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
                <DialogTitle>Add New API Key</DialogTitle>
                <DialogContent>
                    <TextField autoFocus margin="dense" label="API Key Name" type="text" fullWidth value={newKeyName} onChange={(e) => setNewKeyName(e.target.value)} />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setDialogOpen(false)} color="primary">Cancel</Button>
                    <Button onClick={generateApiKey} color="primary" disabled={loading || !newKeyName}>{loading ? <CircularProgress size={24} /> : 'Add'}</Button>
                </DialogActions>
            </Dialog>

            <DeleteDialog open={Boolean(confirmDelete)} onClose={() => setConfirmDelete(null)} onDelete={() => { deleteApiKey(confirmDelete); setConfirmDelete(null); }} />
        </div>
    );
};

export default APIKeys;
