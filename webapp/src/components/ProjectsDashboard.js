import React from 'react';
import { Dialog, DialogTitle, DialogContent, List, ListItem, ListItemText, Accordion, AccordionSummary, AccordionDetails, Tooltip } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import AssessmentIcon from '@mui/icons-material/Assessment';
import { useAppContext } from '../AppContext';

const ProjectsDashboard = ({ open, onClose }) => {
    const { email, projects, selectedProject, setSelectedProject } = useAppContext();

    const handleSelectProject = (projectName) => {
        setSelectedProject(projectName);
        onClose();
    };

    return (
        <Dialog onClose={onClose} open={open} fullWidth maxWidth="md">
            <DialogTitle>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <AssessmentIcon sx={{ marginRight: '4px', fontSize: '30px', color: '#CD5C5C' }} />
                    <span>{email}'s projects</span>
                </div>
            </DialogTitle>
            <DialogContent>
                <List>
                    {projects.map(project => (
                        <ListItem
                            button
                            onClick={() => handleSelectProject(project.project_name)}
                            selected={selectedProject === project.project_name}
                            style={{ cursor: 'pointer' }}
                        >
                            {selectedProject === project.project_name}
                            <ListItemText primary={project.project_name} />
                            <Accordion>
                                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                    <Tooltip title="Project Details">
                                        <span>Details</span>
                                    </Tooltip>
                                </AccordionSummary>
                                <AccordionDetails>
                                    {/* Project specific details */}
                                </AccordionDetails>
                            </Accordion>
                        </ListItem>
                    ))}
                </List>
            </DialogContent>
        </Dialog>
    );
};

export default ProjectsDashboard;