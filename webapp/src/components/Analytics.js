import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAppContext } from '../AppContext';
import { Bar } from 'react-chartjs-2';
import { TimeScale, CategoryScale, LinearScale, BarElement, Chart } from 'chart.js';
import 'chartjs-adapter-date-fns';  // or 'chartjs-adapter-moment'

Chart.register(TimeScale, CategoryScale, LinearScale, BarElement);


const Analytics = () => {
    const { email } = useAppContext();
    const [metrics, setMetrics] = useState(null);
    const [projects, setProjects] = useState([]);
    const [selectedProject, setSelectedProject] = useState("maintainability");
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
            }
        } catch (err) {
            setError("An error occurred");
        }
    };

    const fetchMetrics = async () => {
        try {
            setIsLoading(true);
            const response = await axios.get("/get_metrics", {
                params: { user_email: email, project_name: selectedProject },
                headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
            });

            if (response.status === 200) {
                setMetrics(response.data);
            }
        } catch (err) {
            if (err.response?.status === 404) {
                setError("Metrics not found");
            } else {
                setError("An error occurred");
            }
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (email) {
            fetchProjects();
            fetchMetrics();
        }
    }, [email, selectedProject]);

    const aggregatedMetrics = metrics?.reduce((acc, metric) => {
        const date = metric.timestamp.split('T')[0]; // Extract the date part from ISO string
        const weight = metric.loc;

        acc[date] = acc[date] ? acc[date] : { totalLOC: 0, totalReadability: 0 };

        acc[date].totalLOC += weight;
        acc[date].totalReadability += metric.readability * weight;

        return acc;
    }, {});

    // Calculate weighted average
    const dates = [];
    const avgReadability = [];

    for (const [date, data] of Object.entries(aggregatedMetrics || {})) {
        dates.push(date);
        avgReadability.push(data.totalReadability / data.totalLOC);
    }


    const chartData = {
        labels: dates,
        datasets: [
            {
                label: 'Weighted Avg Readability',
                data: avgReadability,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            },
        ],
    };

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
            },
        },
    };

    return (
        <div>
            <select value={selectedProject} onChange={(e) => setSelectedProject(e.target.value)}>
                {projects.map((project, index) => (
                    <option key={index} value={project.project_name}>
                        {project.project_name}
                    </option>
                ))}
            </select>
            {isLoading ? (
                <p>Loading...</p>
            ) : error ? (
                <p>{error}</p>
            ) : (
                <Bar data={chartData} options={chartOptions} />
            )}
        </div>
    );
};


export default Analytics;
