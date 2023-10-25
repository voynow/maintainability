import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { useAppContext } from '../AppContext';
import Plot from 'react-plotly.js';
import { Container, CircularProgress, Paper, List, ListItem, Typography } from '@mui/material';

const Analytics = () => {
    const { email } = useAppContext();
    const [plotData, setPlotData] = useState(null);
    const [projects, setProjects] = useState([]);
    const [selectedProject, setSelectedProject] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchProjects = async () => {
        try {
            const response = await axios.get("/get_user_projects", {
                params: { user_email: email },
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });
            if (response.status === 200) {
                setProjects(response.data);
                if (selectedProject === null && response.data.length > 0) {
                    setSelectedProject(response.data[0].project_name);
                }
            }
        } catch (err) {
            setError("An error occurred while fetching projects.");
        }
    };

    const fetchMetrics = useCallback(async () => {
        if (!selectedProject) return;
        try {
            setIsLoading(true);
            const response = await axios.get("/get_metrics", {
                params: { user_email: email, project_name: selectedProject },
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });
            if (response.status === 200) {
                setPlotData(response.data);
                setError(null);
            }

        } catch (err) {
            setError(err.response?.status === 404 ? "Metrics not found" : "An error occurred while fetching metrics.");
        } finally {
            setIsLoading(false);
        }
    }, [email, selectedProject]);

    useEffect(() => {
        if (email) {
            fetchProjects();
            fetchMetrics();
        }
    }, [email, selectedProject, fetchMetrics]);

    useEffect(() => {
        console.log("State Update: ", { plotData, isLoading, error });
        if (plotData) {
            console.log("Rendering Plot", plotData);
            console.log("Plotly Layout:", plotData.layout);
            console.log("Plotly Data:", plotData.data);
        }
    }, [plotData, isLoading, error]);

    return (
        <div style={{ display: 'flex', width: '100%', padding: '0 16px' }}>
            <div style={{ flex: 3, padding: '16px' }}>
                {
                    isLoading ? (
                        <CircularProgress />
                    ) : error ? (
                        <Typography variant="h6" color="error">{error}</Typography>
                    ) : plotData ? (
                        <div style={{ width: '100%', height: '80vh' }}>
                            <Plot data={plotData.data} layout={plotData.layout} />
                        </div>
                    ) : null
                }
            </div>
            <div style={{
                flex: 1,
                padding: '10px',
                backgroundColor: '#f9f9f9',
                borderRadius: '8px',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                maxHeight: '600px',  // Max height
                minHeight: '300px',  // Min height
                overflow: 'hidden'   // Hide overflow'
            }}>
                <List>
                    {projects.map((project, index) => (
                        <ListItem
                            button
                            key={index}
                            selected={selectedProject === project.project_name}
                            onClick={() => setSelectedProject(project.project_name)}
                            style={{
                                padding: '10px 20px', // Additional padding
                                borderRadius: '4px', // Slight rounding of corners
                                margin: '4px 0', // Some margin between items
                                backgroundColor: selectedProject === project.project_name ? '#e0e0e0' : 'transparent', // Background change on selection
                                transition: 'background-color 0.2s' // Transition for smoother effect
                            }}
                        >
                            {project.project_name}
                        </ListItem>
                    ))}
                </List>
            </div>
        </div >
    );


};

export default Analytics;
