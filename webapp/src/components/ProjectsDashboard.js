import React, { useEffect, useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Accordion, AccordionSummary, AccordionDetails, Typography } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import api from '../axiosConfig';
import { useAppContext } from '../AppContext';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import { Button as MuiButton, Tooltip } from '@mui/material';


const ProjectsDashboard = ({ open, onClose }) => {
    const { email, projects, setSelectedProject } = useAppContext();
    const [expandedProject, setExpandedProject] = useState(null);
    const [projectDetails, setProjectDetails] = useState({});

    useEffect(() => {
        projects.forEach(project => {
            api.get(`/get_project`, { params: { user_email: email, project_name: project.project_name } })
                .then(response => {
                    setProjectDetails(prevDetails => ({ ...prevDetails, [project.project_name]: response.data }));
                })
                .catch(error => {
                    console.error('Error fetching project details', error);
                });
        });
    }, [projects, email]);

    const handleAccordionChange = (projectName) => (event, isExpanded) => {
        setExpandedProject(isExpanded ? projectName : null);
    };

    const handleSelectProject = (projectName) => {
        setSelectedProject(projectName);
        onClose();
    };

    const handleSetFavorite = (projectName, e) => {
        e.stopPropagation(); // Prevents accordion from toggling
        api.post('/set_favorite_project', { user_email: email, project_name: projectName })
            .then(() => {
                // Update project details to reflect the new favorite
                setProjectDetails(prevDetails => {
                    const updatedDetails = { ...prevDetails };
                    Object.keys(updatedDetails).forEach(key => {
                        updatedDetails[key].favorite = key === projectName;
                    });
                    return updatedDetails;
                });
            })
            .catch(error => {
                console.error('Error setting favorite project', error);
            });
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
                <Typography variant="h6" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    {email}'s Projects
                </Typography>
            </DialogTitle>
            <DialogContent>
                {projects.map(project => (
                    <Accordion key={project.project_name} style={projectStyle} expanded={expandedProject === project.project_name} onChange={handleAccordionChange(project.project_name)}>
                        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                            <Typography variant="subtitle1">{project.project_name}</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                {/* Project Details */}
                                <div>
                                    <p>Created at: {projectDetails[project.project_name]?.created_at}</p>
                                    <p>Favorite: {projectDetails[project.project_name]?.favorite ? 'Yes' : 'No'}</p>
                                    <p>GitHub Username: {projectDetails[project.project_name]?.github_username || 'N/A'}</p>
                                </div>

                                {/* Action Buttons */}
                                <div>
                                    <Tooltip title="Select Project">
                                        <Button variant="outlined" style={buttonStyle} startIcon={<CheckCircleOutlineIcon fontSize="small" />} onClick={() => handleSelectProject(project.project_name)}>
                                            Select
                                        </Button>
                                    </Tooltip>
                                    <Tooltip title="Set as Favorite">
                                        <Button variant="outlined"
                                            style={{
                                                ...buttonStyle,
                                                color: projectDetails[project.project_name]?.favorite ? 'white' : '',
                                                backgroundColor: projectDetails[project.project_name]?.favorite ? '#CD5C5C' : '',
                                                outlineColor: projectDetails[project.project_name]?.favorite ? 'white' : '',

                                            }}
                                            startIcon={<FavoriteBorderIcon fontSize="small" />}
                                            onClick={(e) => handleSetFavorite(project.project_name, e)}>
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
