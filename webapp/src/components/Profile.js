import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Avatar } from '@mui/material';
import { useAppContext } from '../AppContext';
import AccountCircle from '@mui/icons-material/AccountCircle';


const ProfilePopup = ({ open, onClose }) => {
    const { email, logout } = useAppContext();

    return (
        <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
            <DialogTitle>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Avatar style={{ marginRight: '16px' }}>
                        <AccountCircle />
                    </Avatar>
                    <span>{email}'s Profile</span>
                </div>
            </DialogTitle>
            <DialogContent>
                {/* Add additional profile details here */}
            </DialogContent>
            <DialogActions>
                <Button onClick={logout} color="primary">
                    Logout
                </Button>
                <Button onClick={onClose} color="secondary">
                    Close
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default ProfilePopup;
