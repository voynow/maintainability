import React, { useEffect, useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Accordion, AccordionSummary, AccordionDetails, Typography } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import api from '../axiosConfig';
import { useAppContext } from '../AppContext';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import { Tooltip } from '@mui/material';

const ProjectsDashboard = ({ open, onClose }) => {
    const { email, projects, setProjects, selectedProject, setSelectedProject } = useAppContext();
    const [expandedProject, setExpandedProject] = useState(null);

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                const response = await api.get("/list_projects", {
                    params: { user_email: email },
                });
                if (response.status === 200 && response.data.projects) {
                    setProjects(response.data.projects);
                    if (!selectedProject && response.data.projects.length > 0) {
                        setSelectedProject(response.data.projects[0].name);
                    }
                }
            } catch (error) {
                console.error("An error occurred while fetching projects.", error);
            }
        };
        fetchProjects();
    }, [open, email, setProjects, setSelectedProject]);

    const handleAccordionChange = (projectName) => {
        setExpandedProject(expandedProject === projectName ? null : projectName);
    };

    const handleSelectProject = (projectName) => {
        setSelectedProject(projectName);
        onClose();
    };

    const handleSetFavorite = async (projectName, e) => {
        e.stopPropagation();
        try {
            await api.post('/set_favorite_project', { user_email: email, project_name: projectName });
            setProjects(prevProjects => prevProjects.map(project =>
                project.name === projectName ? { ...project, favorite: !project.favorite } : project
            ));
        } catch (error) {
            console.error('Error setting favorite project', error);
        }
    };

    const buttonStyle = {
        minWidth: '30px',
        padding: '6px 8px',
        margin: '0 4px',
    };

    const projectStyle = {
        margin: '2px 0',
        borderRadius: '4px',
        backgroundColor: '#f7f7f7',
        boxShadow: 'none',
        borderBottom: '1px solid #e0e0e0'
    };

    return (
        <Dialog onClose={onClose} open={open} fullWidth maxWidth="md">
            <DialogTitle>
                <Typography variant="subtitle1" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    {email}'s Projects
                </Typography>
            </DialogTitle>
            <DialogContent>
                {projects.map(project => (
                    <Accordion key={project.primary_id} style={projectStyle} expanded={expandedProject === project.name} onChange={() => handleAccordionChange(project.name)}>
                        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                            <Typography variant="subtitle1">{project.name}</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                <div>
                                    <p>Created at: {project.created_at}</p>
                                    <p>Favorite: {project.favorite ? 'Yes' : 'No'}</p>
                                    <p>GitHub Username: {project.github_username || 'N/A'}</p>
                                </div>
                                <div>
                                    <Tooltip title="Select Project">
                                        <Button variant="outlined" style={buttonStyle} startIcon={<CheckCircleOutlineIcon fontSize="small" />} onClick={() => handleSelectProject(project.name)}>
                                            Select
                                        </Button>
                                    </Tooltip>
                                    <Tooltip title="Set as Favorite">
                                        <Button variant="outlined"
                                            style={{
                                                ...buttonStyle,
                                                color: project.favorite ? 'white' : '',
                                                backgroundColor: project.favorite ? '#CD5C5C' : '',
                                                outlineColor: project.favorite ? 'white' : '',

                                            }}
                                            startIcon={<FavoriteBorderIcon fontSize="small" />}
                                            onClick={(e) => handleSetFavorite(project.name, e)}>
                                            Favorite
                                        </Button>
                                    </Tooltip>
                                </div>
                            </div>
                        </AccordionDetails>
                    </Accordion>
                ))}
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Close</Button>
            </DialogActions>
        </Dialog>
    );
};

export default ProjectsDashboard;
