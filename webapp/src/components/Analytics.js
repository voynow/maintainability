import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { useAppContext } from '../AppContext';
import { Bar } from 'react-chartjs-2';
import { TimeScale, CategoryScale, LinearScale, BarElement, Chart } from 'chart.js';
import 'chartjs-adapter-date-fns';

Chart.register(TimeScale, CategoryScale, LinearScale, BarElement);

const Analytics = () => {
    const { email } = useAppContext();
    const [metrics, setMetrics] = useState({});
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
            console.log("API URL: /get_metrics");
            console.log(`Params: user_email=${email}, project_name=${selectedProject}`);
            const response = await axios.get("/get_metrics", {
                params: { user_email: email, project_name: selectedProject },
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });
            if (response.status === 200) {
                console.log("API Response:", response.data);
                setMetrics(response.data);
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

    const aggregatedMetrics = Object.entries(metrics).reduce((acc, [date, metricObj]) => {
        acc[date] = metricObj;
        return acc;
    }, {});

    const dates = Object.keys(aggregatedMetrics);
    const chartOptions = {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'day'
                },
            },
            y: {
                type: 'linear',
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Metric Value'
                }
            },
        },
        maintainAspectRatio: false,
        animation: {
            duration: 1000,
            easing: 'easeInOutCubic',
        },
    };

    const capitalizeFirstLetter = (str) => {
        return str.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    };


    return (
        <div>
            <select value={selectedProject || ''} onChange={(e) => setSelectedProject(e.target.value)}>
                {projects.map((project, index) => (
                    <option key={index} value={project.project_name}>
                        {project.project_name}
                    </option>
                ))}
            </select>
            {
                isLoading ? (
                    <p>Loading...</p>
                ) : error ? (
                    <p>{error}</p>
                ) : (
                    <div>
                        {['readability', 'design_quality', 'testability', 'consistency', 'debug_error_handling'].map((metric, index) => (
                            <div key={index} style={{ overflow: 'hidden', width: '100%', height: '200px', marginBottom: '30px' }}>
                                <h3 style={{
                                    textAlign: 'center',
                                    fontFamily: 'Arial, Helvetica, sans-serif',
                                    fontSize: '1.8em',
                                    color: '#333333'
                                }}>
                                    {capitalizeFirstLetter(metric)}
                                </h3>

                                <Bar
                                    data={{
                                        labels: dates,
                                        datasets: [{
                                            label: metric,
                                            data: dates.map(date => aggregatedMetrics[date][metric]),
                                            backgroundColor: index % 2 === 0 ? '#CD8C8C' : '#CD5C5C',
                                        }],
                                    }}
                                    options={chartOptions}
                                    height={100}
                                    width={400}
                                />
                            </div>
                        ))}
                    </div>
                )
            }
        </div >
    );
};

export default Analytics;
