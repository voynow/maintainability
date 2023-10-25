import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { useAppContext } from '../AppContext';
import Plot from 'react-plotly.js';

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
                setPlotData(JSON.parse(response.data));
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
        <div style={{ textAlign: 'center' }}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
                {projects.map((project, index) => (
                    <div
                        key={index}
                        style={{
                            padding: '10px',
                            margin: '5px',
                            border: selectedProject === project.project_name ? '2px solid #CD5C5C' : '2px solid #cccccc',
                            borderRadius: '5px',
                            cursor: 'pointer'
                        }}
                        onClick={() => setSelectedProject(project.project_name)}
                    >
                        {project.project_name}
                    </div>
                ))}
            </div>

            {
                isLoading ? (
                    <p>Loading...</p>
                ) : error ? (
                    <p>{error}</p>
                ) : plotData ? (
                    <div style={{ width: '100%', margin: 'auto' }}>
                        <Plot data={plotData.data} layout={{ ...plotData.layout, width: 1000, height: 600 }} />
                    </div>
                ) : null
            }
        </div>
    );
};

export default Analytics;
