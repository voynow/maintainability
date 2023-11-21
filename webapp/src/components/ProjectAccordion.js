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
import LinearProgress from '@mui/material/LinearProgress';

const ProjectAccordion = ({ project, onSelectProject, onSetFavorite, onDeleteProject }) => {
    const [isTriggering, setIsTriggering] = useState(false);
    const [metricsConfig, setMetricsConfig] = useState({});
    const [error, setError] = useState('');
    const [latestLog, setLatestLog] = useState(''); // State to hold the latest log message

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

    const [progress, setProgress] = useState({
        isTriggering: false,
        percentage: 0,
        estimatedTime: null
    });

    const extractExtension = (path) => {
        if (!path) return '';

        const lastDotIndex = path.lastIndexOf('.');
        if (lastDotIndex === -1 || lastDotIndex === 0) return '';
        return path.substring(lastDotIndex + 1);
    };

    const insertFileSnapshot = async (project, path, sessionId, fileId, content, lineCount, extension, timestamp) => {
        console.log('Inserting file snapshot into database:', path);
        // await api.post("/insert_file", {
        //     file_id: fileId,
        //     user_email: project.user,
        //     project_name: project.name,
        //     session_id: sessionId,
        //     file_path: path,
        //     file_size: content.length,
        //     loc: lineCount,
        //     extension: extension,
        //     content: content,
        //     timestamp: timestamp
        // });
    };

    const extractFileMetrics = async (fileId, sessionId, path, content, metricsConfig) => {
        for (let metric of Object.keys(metricsConfig)) {
            console.log(path, 'Extracting metric:', metric);
            setLatestLog(`${path} Extracting metric: ${metric}`);
            // await api.post("/extract_metrics", {
            //     file_id: fileId,
            //     session_id: sessionId,
            //     file_path: path,
            //     content: content,
            //     metric_name: metric
            // });
        }
    };

    const fetchProjectStructure = async (project) => {
        console.log('Fetching project structure:', project.name);
        return await api.get("/fetch_repo_structure", {
            params: {
                user: project.github_username,
                repo: project.name
            }
        });
    };

    const processFile = async (path, project, sessionId, metricsConfig) => {
        console.log('Processing file:', path);
        const fileContentResponse = await api.get("/fetch_file_content", {
            params: {
                user: project.github_username,
                repo: project.name,
                path: path
            }
        });
        const content = fileContentResponse.data;
        const file_id = uuidv4();
        const timestamp = new Date().toISOString();
        const extension = extractExtension(path);
        const line_count = content.split('\n').length;

        const checkFileCriteriaResponse = await api.post("/check_file_criteria", null, {
            params: {
                file_path: path,
                extension: extension,
                line_count: line_count
            }
        });

        if (checkFileCriteriaResponse.data.result) {
            await insertFileSnapshot(project, path, sessionId, file_id, content, line_count, extension, timestamp);
            await extractFileMetrics(file_id, sessionId, path, content, metricsConfig);
        } else {
            console.log('Skipping file:', path);
        }
    };

    const retry = async (fn, retries = 3, delay = 1000) => {
        try {
            return await fn();
        } catch (error) {
            if (retries > 0) {
                setTimeout(() => { }, delay);
                return retry(fn, retries - 1, delay);
            } else {
                throw error;
            }
        }
    };

    const handleTriggerRun = async () => {
        setProgress({ isTriggering: true, percentage: 0 });
        setError('');
        try {
            const sessionId = uuidv4();
            const repoStructureResponse = await retry(() => fetchProjectStructure(project));
            const totalFiles = repoStructureResponse.data.length;

            for (let i = 0; i < totalFiles; i++) {
                await retry(() => processFile(repoStructureResponse.data[i], project, sessionId, metricsConfig));

                // Asynchronous state update
                setProgress(prevProgress => ({
                    ...prevProgress,
                    percentage: ((i + 1) / totalFiles) * 100
                }));

                // Optional: artificial delay for visibility
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            setProgress(prevProgress => ({ ...prevProgress, isTriggering: false }));
        } catch (error) {
            console.error('Error triggering project run:', error);
            setProgress({ isTriggering: false, percentage: 0 });
            setError('An error occurred while processing. Please contact the developement team.');
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
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{ flexShrink: 0 }}>
                    <Button
                        startIcon={<PlayCircleOutlineIcon />}
                        onClick={handleTriggerRun}
                        disabled={isTriggering}
                        size="small"
                        variant="outlined"
                        sx={{ margin: 2, width: 'fit-content' }}
                    >
                        Trigger Run
                    </Button>
                </div>
                {error ? (
                    <Typography variant="body2" style={{ color: 'red' }}>
                        {error}
                    </Typography>
                ) : (
                    progress.isTriggering && (
                        <div style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                            <div style={{ width: '100%', position: 'relative' }}>
                                <LinearProgress
                                    variant="determinate"
                                    value={progress.percentage}
                                    style={{
                                        height: '15px',
                                        borderRadius: '5px',
                                        backgroundColor: 'rgba(0,0,0,0.1)',
                                    }}
                                />
                                <Typography variant="body2" style={{
                                    position: 'absolute',
                                    right: 0,
                                    top: '50%',
                                    transform: 'translateY(-50%)',
                                    padding: '0 10px',
                                    backgroundColor: '#fff' // Ensure the text is readable over the progress bar
                                }}>
                                    {`${progress.percentage.toFixed(0)}%`}
                                </Typography>
                            </div>
                            {latestLog && (
                                <Typography variant="caption" style={{ color: '#666', marginTop: '4px' }}>
                                    {latestLog}
                                </Typography>
                            )}
                        </div>
                    )


                )}
            </div>

        </Accordion >
    );
};

export default ProjectAccordion;
