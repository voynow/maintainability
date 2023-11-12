import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Accordion, AccordionSummary, AccordionDetails, ListItemText } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import AssessmentIcon from '@mui/icons-material/Assessment';
import { useAppContext } from '../AppContext';

const ProjectsDashboard = ({ open, onClose }) => {
    const { email, projects, selectedProject, setSelectedProject } = useAppContext();
    const [expandedProject, setExpandedProject] = useState(null);

    const handleAccordionChange = (projectName) => (event, isExpanded) => {
        setExpandedProject(isExpanded ? projectName : null);
    };

    const handleSelectProject = (projectName) => {
        setSelectedProject(projectName);
        onClose();
    };

    const accordionStyle = (projectName) => ({
        margin: '2px 0',
        borderRadius: '4px'
    });

    return (
        <Dialog onClose={onClose} open={open} fullWidth maxWidth="md">
            <DialogTitle>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <AssessmentIcon sx={{ marginRight: '4px', fontSize: '30px', color: '#CD5C5C' }} />
                    <span>{email}'s projects</span>
                </div>
            </DialogTitle>
            <DialogContent>
                {projects.map(project => (
                    <Accordion key={project.id} style={accordionStyle(project.project_name)} expanded={expandedProject === project.project_name} onChange={handleAccordionChange(project.project_name)}>
                        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                            <ListItemText primary={project.project_name} />
                        </AccordionSummary>
                        <AccordionDetails>
                            {/* Insert project specific details here */}
                            <Button onClick={() => handleSelectProject(project.project_name)}>
                                Select This Project
                            </Button>
                        </AccordionDetails>
                    </Accordion>
                ))}
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>
                    Close
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default ProjectsDashboard;
