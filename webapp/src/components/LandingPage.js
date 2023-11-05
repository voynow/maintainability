import React from 'react';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
    const navigate = useNavigate();

    const handleNavigate = (path) => {
        navigate(path);
    };

    return (
        <main className="text-gray-700">
            <section className="flex flex-col items-center justify-center min-h-screen p-4">
                <div className="max-w-4xl mx-auto text-center">
                    <h1 className="text-6xl font-bold mb-6">Maintainability</h1>
                    <p className="text-xl mb-8">
                        Streamline your projects and enhance your productivity. Discover the new age of project management with Maintainability.
                    </p>
                    <div className="flex justify-center gap-4">
                        <button
                            onClick={() => handleNavigate('/signup')}
                            className="px-8 py-3 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 transition duration-300"
                        >
                            Get Started
                        </button>
                        <button
                            onClick={() => handleNavigate('/login')}
                            className="px-8 py-3 border border-blue-600 text-blue-600 text-lg font-semibold rounded-lg hover:bg-blue-50 transition duration-300"
                        >
                            Log In
                        </button>
                    </div>
                </div>
            </section>
            <section className="w-full flex justify-center px-4 py-8 -mt-60">
                <div className="shadow-2xl rounded-lg overflow-hidden">
                    <img src="/landing_page.png" alt="Workflow" className="max-w-5xl w-full h-auto" />
                </div>
            </section>
        </main>
    );
};

export default LandingPage;
