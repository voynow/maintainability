import React, { useEffect, useState, useCallback } from 'react';
import api from '../axiosConfig';
import { useAppContext } from '../AppContext';
import Plot from 'react-plotly.js';
import { CircularProgress, Typography, IconButton, Tooltip, tooltipClasses } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import { styled } from '@mui/material/styles';

const CustomTooltip = styled(({ className, ...props }) => (
    <Tooltip {...props} classes={{ popper: className }} />
))({
    [`& .${tooltipClasses.tooltip}`]: {
        maxWidth: 500,
    },
});

const Analytics = () => {
    const { email, selectedProject, isFetchingProjects } = useAppContext();
    const [plotData, setPlotData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchMetrics = useCallback(async () => {
        if (!selectedProject) {
            if (isFetchingProjects) {
                setIsLoading(true);
                return;
            } else {
                setError("No projects found. Please create a project to view analytics.");
                setIsLoading(false);
                return;
            }
        }

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
    }, [email, selectedProject, isFetchingProjects]);


    useEffect(() => {
        fetchMetrics();
    }, [fetchMetrics]);

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', padding: '0 16px' }}>
            {isLoading ? (
                <CircularProgress />
            ) : error ? (
                <Typography variant="h6" color="error">{error}</Typography>
            ) : plotData ? (
                plotData.map((plot, index) => (
                    <div key={index} style={{ width: '100%', marginBottom: '128px', position: 'relative' }}>
                        <CustomTooltip
                            title={
                                <Typography style={{ whiteSpace: 'pre-line' }}>
                                    {plot.description || "Description unavailable"}
                                </Typography>
                            }
                            placement="bottom"
                            PopperProps={{
                                modifiers: [
                                    {
                                        name: 'offset',
                                        options: {
                                            offset: [0, -25],
                                        },
                                    },
                                ],
                            }}
                        >
                            <IconButton size="large" style={{ color: '#9e9e9e', position: 'absolute', top: 0, left: 0, zIndex: 1000 }}>
                                <InfoIcon fontSize="large" />
                            </IconButton>
                        </CustomTooltip>
                        <Plot
                            data={plot.data}
                            layout={{ ...plot.layout, autosize: true }}
                            style={{ width: '100%', height: '100%' }}
                        />
                    </div>
                ))
            ) : null
            }
        </div>
    );
};
export default Analytics;
