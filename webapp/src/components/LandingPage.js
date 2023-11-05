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
                    <h1 className="text-6xl font-bold text-blue-300">Supercharge Your Codebase</h1>
                    <p className='mt-4 mb-4 text-xl'>
                        Leveraging advanced Language Models, our platform offers a nuanced understanding of code that goes beyond traditional systems.
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
            <section className="w-full flex justify-center px-4 py-8 -mt-40">
                <div className="shadow-2xl rounded-lg overflow-hidden">
                    <img src="/landing_page.png" alt="Workflow" className="max-w-5xl w-full h-auto" />
                </div>
            </section>
        </main >
    );
};

export default LandingPage;
