import React from 'react';
import { useNavigate } from 'react-router-dom';
import SpeedIcon from '@mui/icons-material/Speed';
import AssessmentIcon from '@mui/icons-material/Assessment';
import SettingsIcon from '@mui/icons-material/Settings';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';


const LandingPage = () => {
    const navigate = useNavigate();

    const metrics = [
        {
            title: 'Intuitive Design',
            icon: <AssessmentIcon />,
            summary: 'Emphasizes clear variable/function naming, comment quality, logical code organization, API usability, and code simplicity.'
        },
        {
            title: 'Functional Cohesion',
            icon: <SettingsIcon />,
            summary: 'Focuses on single responsibility, separation of concerns, concise functions, and module cohesion.'
        },
        {
            title: 'Adaptive Resilience',
            icon: <AutorenewIcon />,
            summary: 'Involves comprehensive error-handling, graceful degradation, diligent resource management, and code adaptability.'
        },
        {
            title: 'Code Efficiency',
            icon: <SpeedIcon />,
            summary: 'Covers algorithmic complexity, resource utilization, runtime profiling, concurrency, and optimized data fetching/caching.'
        },
        {
            title: 'Data Integrity',
            icon: <VerifiedUserIcon />,
            summary: 'Includes data validation & sanitation, security of sensitive info, integrity checks, least privilege access, and thorough logging and monitoring.'
        }
    ];

    return (
        <main className="text-gray-700">
            <section className="w-full flex justify-center p-16 pt-32">
                <div className="max-w-4xl mx-auto text-center">
                    <h1 className="text-8xl mb-4 font-bold">
                        Maint<span className="text-red-500">AI</span>nability
                    </h1>
                    <h2 className="text-6xl font-bold text-blue-400 mb-6">The Future of Code Analysis</h2>
                    <p className='mt-6 mb-8 text-xl'>
                        Leveraging advanced Language Models, our platform offers a nuanced understanding of code that goes beyond traditional static code analysis systems.
                    </p>
                    <div className="flex justify-center gap-8 mb-16">
                        <button
                            onClick={() => navigate('/signup')}
                            className="px-10 py-4 bg-white border-2 border-gray-400 text-lg font-semibold rounded-lg hover:bg-blue-100 transition duration-300"
                        >
                            Get Started
                        </button>
                        <button
                            onClick={() => navigate('/login')}
                            className="px-10 py-4 bg-white border-2 border-gray-400 text-lg font-semibold rounded-lg hover:bg-blue-100 transition duration-300"
                        >
                            Log In
                        </button>
                    </div>
                </div>
            </section>
            <section className="w-full flex justify-center p-16">
                <img src="/landing_page.png" alt="Workflow" className="max-w-5xl w-full h-auto" />
            </section>
            <section className="flex justify-center p-16 pb-32">
                <div className="flex flex-col items-center">
                    <div className="flex justify-center gap-8 mb-8">
                        {metrics.slice(0, 3).map((metric, index) => (
                            <div key={index} className="bg-white border-l-4 border-blue-400 shadow-md p-6 rounded-lg flex flex-col items-center" style={{ width: '340px', height: '220px' }}>
                                <div className="flex items-center mb-4">
                                    {metric.icon}
                                    <h3 className="ml-2 text-lg font-semibold">{metric.title}</h3>
                                </div>
                                <p className="text-sm text-gray-600">{metric.summary}</p>
                            </div>
                        ))}
                    </div>
                    <div className="flex justify-center gap-8">
                        {metrics.slice(3, 5).map((metric, index) => (
                            <div key={index} className="bg-white border-l-4 border-blue-400 shadow-md p-6 rounded-lg flex flex-col items-center" style={{ width: '340px', height: '220px' }}>
                                <div className="flex items-center mb-4">
                                    {metric.icon}
                                    <h3 className="ml-2 text-lg font-semibold">{metric.title}</h3>
                                </div>
                                <p className="text-sm text-gray-600">{metric.summary}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>
            <footer className="text-center p-8 text-gray-800">
                <p className="text-sm">
                    &copy; {new Date().getFullYear()} Maintainability. All rights reserved.<br></br>
                    <a href="mailto:voynow99@gmail.com">Contact me</a> or connect on X @jamievoynow
                </p>
            </footer>
        </main>
    );

};

export default LandingPage;