import React from 'react';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
    const navigate = useNavigate();

    return (
        <main className="text-gray-700">
            <section className="flex flex-col items-center justify-center min-h-screen p-4">
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
            <section className="w-full flex justify-center px-4 pt-8 -mt-40 relative">
                <div className="relative shadow-2xl rounded-lg">
                    <img src="/landing_page.png" alt="Workflow" className="max-w-5xl w-full h-auto" />
                    <div className="absolute bottom-0 translate-y-1/2 transform -translate-x-1/2 left-1/2 bg-gray-100 text-gray-700 px-8 py-4 rounded-lg shadow-lg w-full max-w-lg text-left">
                        <h3 className="text-xl font-bold">Example Insights</h3>
                        <p className="text-md mt-1">
                            Out of the box your projects will be evaluated against:
                        </p>
                        <ul className="list-disc pl-6 mt-1 text-md">
                            <li>Intuitive design</li>
                            <li>Functional cohesion</li>
                            <li>And more</li>
                        </ul>
                    </div>
                </div>
            </section>
        </main >
    );
};

export default LandingPage;