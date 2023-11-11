import React from 'react';
import { Dialog, DialogTitle, List, ListItem, ListItemText } from '@mui/material';
import { useAppContext } from '../AppContext';

const ProjectsDashboard = ({ open, onClose }) => {
    const { projects, setSelectedProject } = useAppContext();
    console.log(projects);

    return (
        <Dialog onClose={onClose} open={open}>
            <DialogTitle>Choose a Project</DialogTitle>
            <List>
                {projects && projects.map((project, index) => (
                    <ListItem button onClick={() => {
                        setSelectedProject(project.project_name);
                        onClose();
                    }} key={index}>
                        <ListItemText primary={project.project_name} />
                    </ListItem>
                ))}
            </List>
        </Dialog>
    );
};

export default ProjectsDashboard;
