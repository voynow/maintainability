import React from 'react';
import { useNavigate } from 'react-router-dom';
import SpeedIcon from '@mui/icons-material/Speed';
import AssessmentIcon from '@mui/icons-material/Assessment';
import SettingsIcon from '@mui/icons-material/Settings';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import TwitterIcon from '@mui/icons-material/Twitter';
import GitHubIcon from '@mui/icons-material/GitHub';
import LinkedInIcon from '@mui/icons-material/LinkedIn';

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
            <section className="w-full flex justify-center pt-48">
                <div className="max-w-4xl mx-auto text-center">
                    <h1 className="text-9xl mb-2 font-bold">
                        Maint<span className="text-red-500">AI</span>nability
                    </h1>
                    <h1 className="text-6xl font-bold text-blue-400">The Future of Code Analysis</h1>
                    <p className='mt-4 mb-4 text-2xl'>
                        Leveraging advanced Language Models, our platform offers a nuanced understanding of code that goes beyond traditional static code analysis systems.
                    </p>
                    <div className="flex justify-center gap-4">
                        <button
                            onClick={() => navigate('/signup')}
                            className="px-8 py-3 border-2 bg-white border-gray-400 text-lg text-lg font-semibold rounded-lg hover:bg-blue-100 transition duration-300"
                        >
                            Get Started
                        </button>
                        <button
                            onClick={() => navigate('/login')}
                            className="px-8 py-3 border-2 bg-white border-gray-400 text-lg text-lg font-semibold rounded-lg hover:bg-blue-100 transition duration-300"
                        >
                            Log In
                        </button>
                    </div>
                </div>
            </section>
            <section className="w-full flex justify-center pt-48">
                <div className="relative shadow-2xl rounded-lg">
                    <img src="/landing_page.png" alt="Workflow" className="max-w-5xl w-full h-auto" />
                </div>
            </section>
            <section className="flex justify-center pt-48">
                <div className="flex flex-col items-center">
                    <div className="flex justify-center gap-4 mb-4">
                        {metrics.slice(0, 3).map((metric, index) => (
                            <div key={index} className="bg-white border-l-4 border-blue-400 shadow-md p-4 rounded-lg flex flex-col items-center" style={{ width: '300px', height: '200px' }}>
                                <div className="flex items-center mb-2">
                                    {metric.icon}
                                    <h3 className="ml-2 text-lg font-semibold">{metric.title}</h3>
                                </div>
                                <p className="text-sm text-gray-600">{metric.summary}</p>
                            </div>
                        ))}
                    </div>
                    <div className="flex justify-center gap-4">
                        {metrics.slice(3, 5).map((metric, index) => (
                            <div key={index} className="bg-white border-l-4 border-blue-400 shadow-md p-4 rounded-lg flex flex-col items-center" style={{ width: '300px', height: '200px' }}>
                                <div className="flex items-center mb-2">
                                    {metric.icon}
                                    <h3 className="ml-2 text-lg font-semibold">{metric.title}</h3>
                                </div>
                                <p className="text-sm text-gray-600">{metric.summary}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>
            <section className="pt-24 pb-24"></section>
            <section className="bg-gray-800 text-gray-200 p-4">
                <div className="container mx-auto text-center">
                    <div className="m-10">
                        <h2 className="text-5xl font-bold mb-4">Interested in our mission?</h2>
                        <p className="text-2xl mb-3">
                            Motivated individuals passionate about the future of AI-assisted software development:
                        </p>
                        <p className="text-red-400 font-bold text-3xl mb-8">    
                            Lets connect!
                        </p>
                        <div className="flex justify-center gap-10 mt-20 text-blue-400">
                            <a href="https://twitter.com/jamievoynow" target="_blank" rel="noopener noreferrer" aria-label="Twitter">
                                <TwitterIcon fontSize="large" />
                            </a>
                            <a href="https://github.com/voynow" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
                                <GitHubIcon fontSize="large" />
                            </a>
                            <a href="https://linkedin.com/in/voynow" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
                                <LinkedInIcon fontSize="large" />
                            </a>
                        </div>
                    </div>
                </div>
            </section>
            <footer className="text-center pt-16 pb-2 text-gray-800">
                <p className="text-sm">
                    &copy; {new Date().getFullYear()} Maintainability. All rights reserved.<br></br>
                </p>
            </footer>
        </main>
    );
};

export default LandingPage;