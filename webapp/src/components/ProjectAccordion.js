import React, { useState } from 'react';
import { Accordion, AccordionSummary, AccordionDetails, Typography, IconButton, Tooltip, Button } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import DeleteIcon from '@mui/icons-material/Delete';
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';
import api from '../axiosConfig';

const ProjectAccordion = ({ project, onSelectProject, onSetFavorite, onDeleteProject, api_key }) => {
    const [isTriggering, setIsTriggering] = useState(false);

    const handleTriggerRun = async () => {
        setIsTriggering(true);

        try {
            const repoStructureResponse = await api.get("/fetch_repo_structure", {
                params: {
                    user: project.github_username,
                    repo: project.name
                }
            });

            for (let path of repoStructureResponse.data) {
                const fileContentResponse = await api.get("/fetch_file_content", {
                    params: {
                        user: project.github_username,
                        repo: project.name,
                        path: path
                    }
                });

                const fileContent = fileContentResponse.data;
                const file_id = generateUUID();
                const timestamp = new Date().toISOString();

                await api.post("/insert_file", {
                    file_id,
                    user_email: project.user,
                    project_name: project.name,
                    session_id: generateUUID(),
                    file_path: path,
                    file_size: fileContent.length,
                    loc: fileContent.split('\n').length,
                    extension: extractExtension(path),
                    content: fileContent,
                    timestamp
                });

                for (let metric of config.METRICS) {
                    await api.post("/extract_metrics", {
                        file_id: file_id,
                        filepath: path,
                        file_content: fileContent,
                        metric: metric
                    });
                }
            }
        } catch (error) {
            console.error('Error triggering project run:', error);
        } finally {
            setIsTriggering(false);
        }
    };

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
            <Button
                startIcon={<PlayCircleOutlineIcon />}
                onClick={handleTriggerRun}
                disabled={isTriggering}
                size="small"
                variant="outlined"
                sx={{ margin: 2 }}
            >
                Trigger Run
            </Button>
        </Accordion>
    );
};

export default ProjectAccordion;
