import React from 'react';
import { Dialog, DialogTitle, List, ListItem, ListItemText } from '@mui/material';
import { useAppContext } from '../AppContext';
import CheckIcon from '@mui/icons-material/Check';

const ProjectsDashboard = ({ open, onClose }) => {
    const { projects, selectedProject, setSelectedProject } = useAppContext();

    return (
        <Dialog onClose={onClose} open={open}>
            <DialogTitle>Choose a Project</DialogTitle>
            <List>
                {projects.map((project, index) => (
                    <ListItem
                        button
                        onClick={() => {
                            setSelectedProject(project.project_name);
                            onClose();
                        }}
                        key={index}
                        selected={selectedProject === project.project_name}
                    >
                        <ListItemText primary={project.project_name} />
                        {selectedProject === project.project_name && <CheckIcon />}
                    </ListItem>
                ))}
            </List>
        </Dialog>
    );
};

export default ProjectsDashboard;
