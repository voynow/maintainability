import React, { useEffect, useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, IconButton, Accordion, AccordionSummary, AccordionDetails, Typography, useMediaQuery } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import AssessmentIcon from '@mui/icons-material/Assessment';
import Button from '@mui/material/Button';
import api from '../axiosConfig';
import { useAppContext } from '../AppContext';

const ProjectsDashboard = ({ open, onClose }) => {
    const { email, projects, setProjects, setSelectedProject } = useAppContext();
    const theme = useTheme();
    const isXsScreen = useMediaQuery(theme.breakpoints.down('xs'));

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                const response = await api.get("/list_projects", { params: { user_email: email } });
                if (response.status === 200) {
                    setProjects(response.data.projects);
                }
            } catch (error) {
                console.error("An error occurred while fetching projects.", error);
            }
        };

        fetchProjects();
    }, [open, email, setProjects]);

    const handleSelectProject = (projectName) => {
        setSelectedProject(projectName);
        onClose();
    };

    const handleSetFavorite = async (projectName, e) => {
        e.stopPropagation();
        try {
            await api.post('/set_favorite_project', { user_email: email, project_name: projectName });
            setProjects(prev => prev.map(p => p.name === projectName ? { ...p, favorite: !p.favorite } : p));
        } catch (error) {
            console.error('Error setting favorite project', error);
        }
    };

    return (
        <Dialog onClose={onClose} open={open} fullScreen={isXsScreen} fullWidth={!isXsScreen} maxWidth="md">
            <DialogTitle sx={{ m: 0, p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h6" component="div" sx={{ textAlign: 'center', width: '100%' }}>
                    <AssessmentIcon sx={{ marginRight: '5px', color: '#CD5C5C', fontSize: '32px' }} />
                    {email}'s Projects
                </Typography>
            </DialogTitle>

            <DialogContent dividers>
                {projects.map((project) => (
                    <Accordion key={project.primary_id} elevation={1} square>
                        <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel1a-content" id={`panel1a-header-${project.primary_id}`}>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
                                <Typography variant="subtitle1" sx={{ flexShrink: 0 }}>
                                    {project.name}
                                </Typography>
                                <div>
                                    <IconButton onClick={(e) => handleSetFavorite(project.name, e)} size="small">
                                        {project.favorite ? (
                                            <FavoriteIcon style={{ color: '#CD5C5C' }} />
                                        ) : (
                                            <FavoriteBorderIcon />
                                        )}
                                    </IconButton>
                                    <IconButton onClick={() => handleSelectProject(project.name)} size="small">
                                        <CheckCircleOutlineIcon />
                                    </IconButton>
                                </div>
                            </div>
                        </AccordionSummary>
                        <AccordionDetails>
                            <Typography variant="body2">
                                Created at: {new Date(project.created_at).toLocaleDateString()}
                                <br />
                                GitHub Username: {project.github_username || 'Not provided'}
                            </Typography>
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
