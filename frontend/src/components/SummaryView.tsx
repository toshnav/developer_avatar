import React from 'react';
import ReactMarkdown from 'react-markdown';
import { ActivitySummary } from '@/lib/types';
import { StatusCard } from './StatusCard';

interface SummaryViewProps {
    summary: ActivitySummary;
}

export const SummaryView: React.FC<SummaryViewProps> = ({ summary }) => {
    return (
        <div className="space-y-6 animate-fade-in-up">
            {/* Status Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <StatusCard
                    title="Status"
                    value={summary.status}
                    colorClass={summary.status === 'Blocked' ? 'text-red-400' : 'text-green-400'}
                />
                <StatusCard
                    title="Total Hours"
                    value={`${summary.total_hours.toFixed(2)} hrs`}
                    colorClass="text-blue-400"
                />
                <StatusCard
                    title="Issues"
                    value={summary.issues_worked_on.length}
                    colorClass="text-yellow-400"
                />
            </div>

            {/* Detailed Table (New V2 Feature) */}
            {summary.details && summary.details.length > 0 && (
                <div className="bg-gray-800 rounded-2xl border border-gray-700 shadow-lg overflow-hidden">
                    <div className="px-6 py-4 border-b border-gray-700 bg-gray-800/50">
                        <h3 className="text-lg font-semibold text-gray-200">Work Log Details</h3>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-gray-300">
                            <thead className="bg-gray-900/50 text-gray-400 uppercase text-xs">
                                <tr>
                                    <th className="px-6 py-3">Key</th>
                                    <th className="px-6 py-3">Summary</th>
                                    <th className="px-6 py-3">Status</th>
                                    <th className="px-6 py-3">Time</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-700">
                                {summary.details.map((issue) => (
                                    <tr key={issue.key} className="hover:bg-gray-700/30 transition-colors">
                                        <td className="px-6 py-4 font-mono text-sm text-purple-300">{issue.key}</td>
                                        <td className="px-6 py-4">{issue.summary}</td>
                                        <td className="px-6 py-4 text-sm">
                                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${issue.status === 'Done' ? 'bg-green-900/50 text-green-300' :
                                                    issue.status === 'In Progress' ? 'bg-blue-900/50 text-blue-300' : 'bg-gray-700 text-gray-300'
                                                }`}>
                                                {issue.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 font-mono text-sm">{issue.time_spent.toFixed(2)}h</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}

            {/* AI Summary */}
            <div className="bg-gradient-to-br from-gray-800 to-gray-900 p-8 rounded-2xl border border-teal-900/30 shadow-2xl relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4 opacity-10">
                    <svg className="w-32 h-32 text-teal-400" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" /></svg>
                </div>
                <h3 className="text-xl font-semibold mb-4 text-teal-300 flex items-center gap-2">
                    <span>✨</span> Agent Summary
                </h3>
                <div className="prose prose-invert max-w-none text-gray-300 leading-relaxed">
                    <ReactMarkdown>{summary.summary}</ReactMarkdown>
                </div>
            </div>
        </div>
    );
};
