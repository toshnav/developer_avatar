'use client';
import React, { useEffect } from 'react';

interface ActivityInputProps {
    email: string;
    setEmail: (email: string) => void;
    date: string;
    setDate: (date: string) => void;
    llmProvider: string;
    setLlmProvider: (provider: string) => void;
    onFetch: () => void;
    loading: boolean;
    error: string | null;
}

export const ActivityInput: React.FC<ActivityInputProps> = ({
    email, setEmail, date, setDate, llmProvider, setLlmProvider, onFetch, loading, error
}) => {

    // Persistence Effect
    useEffect(() => {
        const savedEmail = localStorage.getItem('developer_email');
        const savedProvider = localStorage.getItem('llm_provider');
        if (savedEmail) setEmail(savedEmail);
        if (savedProvider) setLlmProvider(savedProvider);
    }, [setEmail, setLlmProvider]);

    // Save on change
    const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const val = e.target.value;
        setEmail(val);
        localStorage.setItem('developer_email', val);
    };

    const handleProviderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const val = e.target.value;
        setLlmProvider(val);
        localStorage.setItem('llm_provider', val);
    };

    return (
        <div className="bg-gray-800 p-8 rounded-2xl shadow-xl border border-gray-700 backdrop-blur-sm bg-opacity-80">
            <h2 className="text-2xl font-semibold mb-6 text-purple-300">Daily Check-in</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label className="block text-sm font-medium text-gray-400 mb-2">Developer Email</label>
                    <input
                        type="email"
                        className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-500 transition-all"
                        placeholder="dev@example.com"
                        value={email}
                        onChange={handleEmailChange}
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-400 mb-2">Date</label>
                    <input
                        type="date"
                        className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 text-white transition-all"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                    />
                </div>
            </div>

            <div className="mt-4">
                <label className="block text-sm font-medium text-gray-400 mb-2">AI Provider</label>
                <div className="flex space-x-4">
                    <label className="inline-flex items-center cursor-pointer">
                        <input type="radio" className="form-radio text-purple-600 focus:ring-purple-500 bg-gray-700 border-gray-600" name="provider" value="azure" checked={llmProvider === 'azure'} onChange={handleProviderChange} />
                        <span className="ml-2 text-gray-300">Azure OpenAI</span>
                    </label>
                    <label className="inline-flex items-center cursor-pointer">
                        <input type="radio" className="form-radio text-purple-600 focus:ring-purple-500 bg-gray-700 border-gray-600" name="provider" value="groq" checked={llmProvider === 'groq'} onChange={handleProviderChange} />
                        <span className="ml-2 text-gray-300">Groq</span>
                    </label>
                    <label className="inline-flex items-center cursor-pointer">
                        <input type="radio" className="form-radio text-purple-600 focus:ring-purple-500 bg-gray-700 border-gray-600" name="provider" value="openai" checked={llmProvider === 'openai'} onChange={handleProviderChange} />
                        <span className="ml-2 text-gray-300">OpenAI</span>
                    </label>
                </div>
            </div>

            <button
                onClick={onFetch}
                disabled={loading}
                className={`mt-8 w-full py-4 rounded-xl font-bold text-lg tracking-wide shadow-lg transform transition-all hover:scale-[1.02] ${loading
                    ? 'bg-gray-600 cursor-not-allowed'
                    : 'bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white'
                    }`}
            >
                {loading ? 'Analyzing Worklogs...' : 'Generate Status Report'}
            </button>
            {error && <p className="text-red-400 mt-4 text-center bg-red-900/20 py-2 rounded-lg border border-red-900/50">{error}</p>}
        </div>
    );
};
