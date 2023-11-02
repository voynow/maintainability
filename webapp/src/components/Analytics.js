import React, { useEffect, useState, useCallback } from 'react';
import api from '../axiosConfig';
import { useAppContext } from '../AppContext';
import Plot from 'react-plotly.js';
import { CircularProgress, Typography } from '@mui/material';
import { Tooltip, IconButton } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';


const Analytics = () => {
    const { email, selectedProject } = useAppContext();
    const [plotData, setPlotData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchMetrics = useCallback(async () => {
        if (!selectedProject) return;
        try {
            setIsLoading(true);
            const response = await api.get("/get_metrics", {
                params: { user_email: email, project_name: selectedProject },
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
        if (email && selectedProject) {
            fetchMetrics();
        }
    }, [email, selectedProject, fetchMetrics]);

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', padding: '0 16px' }}>
            {
                isLoading ? (
                    <CircularProgress />
                ) : error ? (
                    <Typography variant="h6" color="error">{error}</Typography>
                ) : plotData && (
                    plotData.map((plot, index) => (
                        <div key={index} style={{ width: '100%', marginBottom: '128px', position: 'relative' }}>
                            <Tooltip title={plot.description || "Description unavailable"}>
                                <IconButton
                                    aria-label="info"
                                    size="large"
                                    style={{
                                        position: 'absolute',
                                        top: 0,
                                        left: 0,
                                        color: '#9e9e9e', // modern light grey
                                        zIndex: 1000
                                    }}
                                >
                                    <InfoIcon fontSize="large" />
                                </IconButton>
                            </Tooltip>
                            <Plot
                                data={plot.data}
                                layout={{ ...plot.layout, autosize: true }}
                                style={{ width: '100%', height: '100%' }}
                            />
                        </div>
                    ))
                )
            }
        </div>
    );
};

export default Analytics;
