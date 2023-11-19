import React from 'react';
import { Accordion, AccordionSummary, AccordionDetails, Typography, IconButton, Tooltip } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import DeleteIcon from '@mui/icons-material/Delete';

const ProjectAccordion = ({ project, onSelectProject, onSetFavorite, onDeleteProject }) => {
    return (
        <Accordion key={project.primary_id} elevation={1} square>
            <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls={`panel-content-${project.primary_id}`} id={`panel-header-${project.primary_id}`}>
                <Typography variant="subtitle1" sx={{ flexShrink: 0 }}>
                    {project.name}
                </Typography>
            </AccordionSummary>
            <AccordionDetails sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <Typography variant="body2">
                        Created at: {new Date(project.created_at).toLocaleDateString()}
                        <br />
                        GitHub Username: {project.github_username || 'Not provided'}
                    </Typography>
                </div>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                    <Tooltip title="Select Project">
                        <IconButton onClick={() => onSelectProject(project.name)} size="small">
                            <CheckCircleOutlineIcon />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title={project.favorite ? "Unset as Favorite" : "Set as Favorite"}>
                        <IconButton onClick={(e) => onSetFavorite(project.name, e)} size="small">
                            {project.favorite ? <FavoriteIcon style={{ color: '#CD5C5C' }} /> : <FavoriteBorderIcon />}
                        </IconButton>
                    </Tooltip>
                    <Tooltip title="Delete Project">
                        <IconButton onClick={(e) => onDeleteProject(project.name, project.github_username, e)} size="small">
                            <DeleteIcon />
                        </IconButton>
                    </Tooltip>
                </div>
            </AccordionDetails>
        </Accordion>
    );
};

export default ProjectAccordion;
