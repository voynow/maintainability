import React, { useEffect, useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Typography, useMediaQuery, Button, LinearProgress, Tooltip, Zoom, IconButton, TextField, InputAdornment } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import AssessmentIcon from '@mui/icons-material/Assessment';
import AddIcon from '@mui/icons-material/Add';
import CheckIcon from '@mui/icons-material/Check';
import AccountCircle from '@mui/icons-material/AccountCircle';
import StorageIcon from '@mui/icons-material/Storage';
import api from '../axiosConfig';
import { useAppContext } from '../AppContext';
import ProjectAccordion from './ProjectAccordion';

const ProjectsDashboard = ({ open, onClose }) => {
    const { email, projects, setProjects, selectedProject, setSelectedProject, isFetchingProjects, setIsFetchingProjects } = useAppContext();
    const [githubUsername, setGithubUsername] = useState('');
    const [githubRepo, setGithubRepo] = useState('');
    const [addProjectError, setAddProjectError] = useState('');
    const [addingProject, setAddingProject] = useState(false);
    const [operationInProgress, setOperationInProgress] = useState(false);

    const theme = useTheme();
    const isXsScreen = useMediaQuery(theme.breakpoints.down('xs'));

    useEffect(() => {
        if (!projects.length) {
            fetchProjects();
        }
    }, [open, email, setProjects, setSelectedProject]);

    const fetchProjects = async () => {
        try {

            const response = await api.get("/list_projects", { params: { user_email: email } });
            if (response.status === 200) {
                // Check if the response data for projects is null
                if (response.data.projects === null) {
                    setProjects([]);
                    setSelectedProject(null);
                } else {
                    setProjects(response.data.projects);
                    // Find a favorite project or default to the first project
                    const favoriteProject = response.data.projects.find(p => p.favorite);
                    setSelectedProject(favoriteProject ? favoriteProject.name : response.data.projects[0]?.name);
                }
            }
        } catch (error) {
            console.error("An error occurred while fetching projects.", error);
            setProjects([]);
            setSelectedProject(null);
        } finally {
            setIsFetchingProjects(false);
        }
    };

    const handleSelectProject = projectName => {
        setSelectedProject(projectName);
        onClose();
    };

    const handleSetFavorite = async (projectName, e) => {
        e.stopPropagation();

        // If the project is already favorited, do nothing
        const currentProject = projects.find(p => p.name === projectName);
        if (currentProject && currentProject.favorite) {
            return;
        }

        try {
            await api.post('/set_favorite_project', { user_email: email, project_name: projectName });

            // Set the selected project as favorite and remove favorite from all others
            setProjects(prevProjects =>
                prevProjects.map(p =>
                    p.name === projectName
                        ? { ...p, favorite: true } // Set the selected project as favorite
                        : { ...p, favorite: false } // Remove favorite from all other projects
                )
            );
        } catch (error) {
            console.error('Error setting favorite project', error);
        }
    };

    const handleDeleteProject = async (githubRepo, githubUsername, e) => {
        e.stopPropagation();
        setOperationInProgress(true);
        // Optional: show confirmation dialog before proceeding

        try {
            console.log('Deleting project:', email, githubRepo, githubUsername);
            const response = await api.post("/delete_project", null, {
                params: {
                    user: email,
                    github_username: githubUsername,
                    github_repo: githubRepo
                }
            });

            // Handle the response, refresh project list if necessary
            if (response.status === 200) {
                fetchProjects(); // Refresh the projects list
            }
        } catch (error) {
            console.error('Error deleting project:', error);
        } finally {
            setOperationInProgress(false);
        }
    };

    const handleToggleAddProject = () => {
        setAddingProject(prev => !prev);
    };

    const handleAddProject = async (e) => {
        e.preventDefault();
        setAddProjectError('');
        setOperationInProgress(true);

        try {
            // Insert project into the database
            const insertResponse = await api.post("/insert_project", null, {
                params: {
                    user: email,
                    github_username: githubUsername,
                    github_repo: githubRepo
                }
            });

            if (insertResponse.status === 200) {
                await fetchProjects();
                setGithubUsername('');
                setGithubRepo('');
                setAddingProject(false);
            }
        } catch (error) {
            console.error('Error adding project:', error);

            // Check if the error response and data are available and log them
            if (error.response && error.response.data) {
                console.error('Validation errors:', error.response.data);
                // If your server sends back a JSON with error messages, you can log them like this
                // If the error details are in a specific property, adjust the key accordingly
                const errorDetails = error.response.data.detail || error.response.data.errors;
                console.error('Error details:', errorDetails);

                // Update the state with the error message to display to the user if needed
                setAddProjectError('Failed to add project. ' + (errorDetails || error.message));
            } else {
                // Fallback error message
                setAddProjectError('Failed to add project. An unexpected error occurred.');
            }
        } finally {
            setOperationInProgress(false);
        }
    };

    const handleClose = () => {
        setAddingProject(false);
        onClose();
    };

    return (
        <Dialog onClose={handleClose} open={open} fullScreen={isXsScreen} fullWidth={!isXsScreen} maxWidth="md">
            {operationInProgress && <LinearProgress />}
            <DialogTitle sx={{ m: 0, p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h5" component="div" sx={{ textAlign: 'center', width: '100%' }}>
                    <AssessmentIcon sx={{ marginRight: '5px', color: '#CD5C5C', fontSize: '32px' }} />
                    {email}'s Projects
                </Typography>
            </DialogTitle>

            <DialogContent dividers>
                {projects.map(project => (
                    <ProjectAccordion
                        key={project.primary_id}
                        project={project}
                        onSelectProject={handleSelectProject}
                        onSetFavorite={handleSetFavorite}
                        onDeleteProject={handleDeleteProject}
                    />
                ))}
                {addingProject ? (
                    <Zoom in={addingProject}>
                        <form onSubmit={handleAddProject} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '20px' }}>
                            <TextField
                                label="GitHub Username"
                                variant="standard"
                                value={githubUsername}
                                onChange={(e) => setGithubUsername(e.target.value)}
                                helperText="Enter your GitHub username."
                                InputProps={{
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <AccountCircle />
                                        </InputAdornment>
                                    ),
                                }}
                            />
                            <TextField
                                label="GitHub Repository"
                                variant="standard"
                                value={githubRepo}
                                onChange={(e) => setGithubRepo(e.target.value)}
                                helperText="Enter your GitHub repository name."
                                InputProps={{
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <StorageIcon />
                                        </InputAdornment>
                                    ),
                                }}
                            />
                            <IconButton type="submit" color="primary" aria-label="add project">
                                <CheckIcon />
                            </IconButton>
                        </form>
                    </Zoom>
                ) : (
                    <Tooltip title="Add New Project">
                        <IconButton onClick={handleToggleAddProject} color="primary" aria-label="add project" size="large">
                            <AddIcon fontSize="large" />
                        </IconButton>
                    </Tooltip>
                )}
                {addProjectError && (
                    <Typography color="error" align="left">
                        {addProjectError}
                    </Typography>
                )}
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose}>Close</Button>
            </DialogActions>
        </Dialog>
    );
};

export default ProjectsDashboard;
