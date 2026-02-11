'use client';

import { useState } from 'react';
import { fetchActivitySummary } from '@/lib/api';
import { ActivitySummary } from '@/lib/types';

export default function Home() {
  const [email, setEmail] = useState('');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [summary, setSummary] = useState<ActivitySummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFetch = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchActivitySummary(email, date);
      setSummary(data);
    } catch (err) {
      setError('Failed to fetch data. Please check backend connection and inputs.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 font-sans p-8">
      <header className="mb-12 text-center">
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
          Autum
        </h1>
        <p className="text-gray-400 mt-2 text-lg">Your AI Developer Avatar</p>
      </header>

      <main className="max-w-4xl mx-auto space-y-8">
        {/* Input Section */}
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
                onChange={(e) => setEmail(e.target.value)}
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
          <button
            onClick={handleFetch}
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

        {/* Results Section */}
        {summary && (
          <div className="space-y-6 animate-fade-in-up">
            {/* Status Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-lg">
                <h3 className="text-sm uppercase tracking-wider text-gray-400 mb-1">Status</h3>
                <p className={`text-2xl font-bold ${summary.status === 'Blocked' ? 'text-red-400' : 'text-green-400'}`}>
                  {summary.status}
                </p>
              </div>
              <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-lg">
                <h3 className="text-sm uppercase tracking-wider text-gray-400 mb-1">Total Hours</h3>
                <p className="text-2xl font-bold text-blue-400">{summary.total_hours.toFixed(2)} hrs</p>
              </div>
              <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-lg">
                <h3 className="text-sm uppercase tracking-wider text-gray-400 mb-1">Issues</h3>
                <p className="text-2xl font-bold text-yellow-400">{summary.issues_worked_on.length}</p>
              </div>
            </div>

            {/* AI Summary */}
            <div className="bg-gradient-to-br from-gray-800 to-gray-900 p-8 rounded-2xl border border-teal-900/30 shadow-2xl relative overflow-hidden">
              <div className="absolute top-0 right-0 p-4 opacity-10">
                <svg className="w-32 h-32 text-teal-400" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" /></svg>
              </div>
              <h3 className="text-xl font-semibold mb-4 text-teal-300 flex items-center gap-2">
                <span>✨</span> Agent Summary
              </h3>
              <div className="prose prose-invert max-w-none text-gray-300 leading-relaxed whitespace-pre-line">
                {summary.summary}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
