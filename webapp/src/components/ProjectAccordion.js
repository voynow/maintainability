import { useState, useEffect } from 'react';
import { Accordion, AccordionSummary, AccordionDetails, Typography, IconButton, Tooltip, Button } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import DeleteIcon from '@mui/icons-material/Delete';
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';
import api from '../axiosConfig';
import { v4 as uuidv4 } from 'uuid';

const ProjectAccordion = ({ project, onSelectProject, onSetFavorite, onDeleteProject }) => {
    const [isTriggering, setIsTriggering] = useState(false);
    const [metricsConfig, setMetricsConfig] = useState({});

    useEffect(() => {
        // Fetch metrics config when component mounts
        const fetchMetricsConfig = async () => {
            try {
                const response = await api.get("/get_metrics_config");
                setMetricsConfig(response.data);
            } catch (error) {
                console.error('Error fetching metrics config:', error);
            }
        };

        fetchMetricsConfig();
    }, []);

    const handleTriggerRun = async () => {
        setIsTriggering(true);

        try {
            // Generating a random UUID
            const session_id = uuidv4();

            // retieving project structure from github/com/project.github_username/project.name
            const repoStructureResponse = await api.get("/fetch_repo_structure", {
                params: {
                    user: project.github_username,
                    repo: project.name
                }
            });

            // Iterating over each file in the project structure
            for (let path of repoStructureResponse.data) {
                const fileContentResponse = await api.get("/fetch_file_content", {
                    params: {
                        user: project.github_username,
                        repo: project.name,
                        path: path
                    }
                });

                // Extracting file content & metadata
                const fileContent = fileContentResponse.data;
                const file_id = uuidv4();
                const timestamp = new Date().toISOString();

                // Insert file snapshot into database
                await api.post("/insert_file", {
                    file_id,
                    user_email: project.user,
                    project_name: project.name,
                    session_id: session_id,
                    file_path: path,
                    file_size: fileContent.length,
                    loc: fileContent.split('\n').length,
                    extension: extractExtension(path),
                    content: fileContent,
                    timestamp
                });

                // Extracting metrics for each file using the keys of the metrics config
                for (let metric of Object.keys(metricsConfig)) {
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
