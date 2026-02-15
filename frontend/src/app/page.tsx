'use client';

import { useState } from 'react';
import { fetchActivitySummary } from '@/lib/api';
import { ActivitySummary } from '@/lib/types';
import Link from 'next/link';
import { ActivityInput } from '../components/ActivityInput';
import { SummaryView } from '../components/SummaryView';

export default function Home() {
  const [email, setEmail] = useState('');
  // Use local date instead of UTC to avoid timezone issues
  const [date, setDate] = useState(() => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  });
  const [llmProvider, setLlmProvider] = useState('azure');
  const [summary, setSummary] = useState<ActivitySummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFetch = async () => {
    if (!email) {
      setError("Please enter an email address.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await fetchActivitySummary(email, date, llmProvider);
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
      <header className="mb-12 text-center relative">
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
          Autum
        </h1>
        <p className="text-gray-400 mt-2 text-lg">Your AI Developer Avatar</p>
        <div className="absolute right-0 top-0">
          <Link href="/timesheet" className="text-sm bg-gray-800 hover:bg-gray-700 text-purple-300 py-2 px-4 rounded border border-purple-500/30 transition-colors">
            Go to Timesheet Generator →
          </Link>
        </div>
      </header>

      <main className="max-w-4xl mx-auto space-y-8">
        <ActivityInput
          email={email}
          setEmail={setEmail}
          date={date}
          setDate={setDate}
          llmProvider={llmProvider}
          setLlmProvider={setLlmProvider}
          onFetch={handleFetch}
          loading={loading}
          error={error}
        />

        {summary && <SummaryView summary={summary} />}
      </main>
    </div>
  );
}
