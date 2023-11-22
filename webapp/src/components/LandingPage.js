import React from 'react';
import { useNavigate } from 'react-router-dom';
import SpeedIcon from '@mui/icons-material/Speed';
import CodeIcon from '@mui/icons-material/Code';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import InsightsIcon from '@mui/icons-material/Insights';
import LayersIcon from '@mui/icons-material/Layers';

const LandingPage = () => {
    const navigate = useNavigate();

    const metrics = [
        {
            title: 'Intuitive Design',
            summary: 'Streamlined user interfaces that enhance user experience and engagement.',
            icon: <InsightsIcon />,
        },
        {
            title: 'Functional Cohesion',
            summary: 'Highly cohesive code modules that improve maintainability and scalability.',
            icon: <LayersIcon />,
        },
        {
            title: 'Performance Efficiency',
            summary: 'Optimized code for the fastest execution and responsiveness.',
            icon: <SpeedIcon />,
        },
        {
            title: 'Code Quality',
            summary: 'Adherence to best coding practices and standards.',
            icon: <CodeIcon />,
        },
        {
            title: 'Growth Potential',
            summary: 'Scalability and adaptability of the codebase for future growth.',
            icon: <TrendingUpIcon />,
        }
    ];

    return (
        <main className="text-gray-700">
            <section className="flex flex-col items-center justify-center min-h-screen p-4 -mt-16">
                <div className="max-w-4xl mx-auto text-center">
                    <h1 className="text-8xl mb-2 font-bold">
                        Maint<span className="text-red-500">AI</span>nability
                    </h1>
                    <h1 className="text-6xl font-bold text-blue-300">The Future of Code Analysis</h1>
                    <p className='mt-4 mb-4 text-xl'>
                        Leveraging advanced Language Models, our platform offers a nuanced understanding of code that goes beyond traditional static code analysis systems.
                    </p>
                    <div className="flex justify-center gap-4">
                        <button
                            onClick={() => navigate('/signup')}
                            className="px-8 py-3 border-2 border-gray-300 text-lg text-lg font-semibold rounded-lg hover:bg-gray-100 transition duration-300"
                        >
                            Get Started
                        </button>
                        <button
                            onClick={() => navigate('/login')}
                            className="px-8 py-3 border-2 border-gray-300 text-lg text-lg font-semibold rounded-lg hover:bg-gray-100 transition duration-300"
                        >
                            Log In
                        </button>
                    </div>
                </div>
            </section>
            <section className="w-full flex justify-center px-4 pt-8 -mt-32 relative pb-32">
                <div className="relative shadow-2xl rounded-lg">
                    <img src="/landing_page.png" alt="Workflow" className="max-w-5xl w-full h-auto" />
                </div>
            </section>
            <section className="flex justify-center p-4">
                <div className="flex flex-row flex-wrap justify-center gap-4">
                    {metrics.map((metric, index) => (
                        <div key={index} className="flex-none bg-white border-l-4 border-blue-500 shadow-md p-4">
                            <div className="flex items-center mb-2">
                                {metric.icon}
                                <h3 className="ml-2 text-lg font-semibold">{metric.title}</h3>
                            </div>
                            <p className="text-sm text-gray-600">{metric.summary}</p>
                        </div>
                    ))}
                </div>
            </section>
            <footer className="text-center p-4 text-gray-800">
                <p className="text-sm">
                    &copy; {new Date().getFullYear()} Maintainability. All rights reserved. Contact: voynow99@gmail.com, @jamievoynow on X.com
                </p>
            </footer>
        </main>
    );
};

export default LandingPage;