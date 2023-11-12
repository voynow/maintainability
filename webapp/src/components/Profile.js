import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import APIKeys from './APIKeys';
import Payments from './Payments';
import { useAppContext } from '../AppContext';

const ProfilePopup = ({ open, onClose }) => {
    const { email, logout } = useAppContext();

    return (
        <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
            <DialogTitle>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <AccountCircleIcon sx={{ marginRight: '4px', fontSize: '30px', color: '#CD5C5C' }} />
                    <span>{email}'s profile</span>
                </div>
            </DialogTitle>
            <DialogContent>
                <Accordion>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        API Keys
                    </AccordionSummary>
                    <AccordionDetails>
                        <APIKeys />
                    </AccordionDetails>
                </Accordion>
                <Accordion>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        Payments
                    </AccordionSummary>
                    <AccordionDetails>
                        <Payments />
                    </AccordionDetails>
                </Accordion>
            </DialogContent>
            <DialogActions>
                <Button onClick={logout}>
                    Logout
                </Button>
                <Button onClick={onClose}>
                    Close
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default ProfilePopup;
