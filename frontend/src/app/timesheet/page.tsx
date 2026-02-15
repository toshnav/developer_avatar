'use client';

import { useState, useEffect } from 'react';

import Link from 'next/link';

interface TimesheetEntry {
    date: string;
    project: string;
    task: string;
    task_description: string;
    status: string;
    remark: string;
    hours: string;
    billable: string;
    role: string;
    site: string;
}

export default function TimesheetPage() {
    const [loading, setLoading] = useState(false);
    const [entries, setEntries] = useState<TimesheetEntry[]>([]);
    const [config, setConfig] = useState({
        jira_email: '',
        jira_project_key: 'PROJ',
        github_username: '',
        github_token: '',
        days: 5,
        employee_id: '',
        employee_name: '',
        billable: 'Yes',
        role: 'Developer',
        site: 'Offshore',
        authorized_hours: '8',
        llm_provider: 'azure'
    });

    // Load config from localStorage on mount
    useEffect(() => {
        const savedConfig = localStorage.getItem('timesheet_config');
        if (savedConfig) {
            setConfig(prev => ({ ...prev, ...JSON.parse(savedConfig) }));
        } else {
            // Fallback to developer_email if available
            const devEmail = localStorage.getItem('developer_email');
            if (devEmail) setConfig(prev => ({ ...prev, jira_email: devEmail }));
        }
    }, []);

    // Save config to localStorage on change
    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const newConfig = { ...config, [e.target.name]: e.target.value };
        setConfig(newConfig);
        localStorage.setItem('timesheet_config', JSON.stringify(newConfig));
    };

    const handleEntryChange = (index: number, field: keyof TimesheetEntry, value: string) => {
        const newEntries = [...entries];
        newEntries[index] = { ...newEntries[index], [field]: value };
        setEntries(newEntries);
    };

    const generateTimesheet = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/timesheet/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config),
            });

            if (!response.ok) {
                throw new Error('Failed to generate timesheet');
            }

            const data = await response.json();
            setEntries(data);
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to generate timesheet. See console for details.');
        } finally {
            setLoading(false);
        }
    };

    const downloadCSV = () => {
        const headers = ['Date', 'Project', 'Task', 'Description', 'Status', 'Remark', 'Hours', 'Billable', 'Role', 'Site', 'Employee ID', 'Employee Name'];
        const csvContent = [
            headers.join(','),
            ...entries.map(e => [
                e.date,
                e.project,
                `"${e.task.replace(/"/g, '""')}"`,
                `"${e.task_description.replace(/"/g, '""')}"`,
                e.status,
                `"${e.remark.replace(/"/g, '""')}"`,
                e.hours,
                e.billable,
                e.role,
                e.site,
                config.employee_id,
                config.employee_name
            ].join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `timesheet_${new Date().toISOString().split('T')[0]}.csv`;
        link.click();
    };

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-[95%] mx-auto">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Timesheet Generator</h1>
                    <Link href="/" className="text-blue-600 hover:text-blue-800">← Back to Dashboard</Link>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                    {/* Configuration Sidebar */}
                    <div className="bg-white p-6 rounded-lg shadow-sm h-fit md:col-span-1">
                        <h2 className="text-lg font-semibold mb-4">Configuration</h2>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Jira Email</label>
                                <input
                                    type="email"
                                    name="jira_email"
                                    value={config.jira_email}
                                    onChange={handleChange}
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Jira Project Key</label>
                                <input
                                    type="text"
                                    name="jira_project_key"
                                    value={config.jira_project_key}
                                    onChange={handleChange}
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">GitHub Username</label>
                                <input
                                    type="text"
                                    name="github_username"
                                    value={config.github_username}
                                    onChange={handleChange}
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">GitHub Token</label>
                                <input
                                    type="password"
                                    name="github_token"
                                    value={config.github_token}
                                    onChange={handleChange}
                                    placeholder="(Optional if set in .env)"
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                                />
                            </div>
                            <div className="border-t pt-4">
                                <h3 className="text-md font-medium mb-2">AI Settings</h3>
                                <select
                                    name="llm_provider"
                                    value={config.llm_provider}
                                    onChange={handleChange}
                                    className="w-full text-sm border p-2 rounded mb-2 bg-white"
                                >
                                    <option value="azure">Azure OpenAI</option>
                                    <option value="groq">Groq</option>
                                    <option value="openai">OpenAI</option>
                                </select>
                            </div>

                            <div className="border-t pt-4">
                                <h3 className="text-md font-medium mb-2">Employee Details</h3>
                                <div className="space-y-2">
                                    <input type="text" name="employee_id" value={config.employee_id} onChange={handleChange} placeholder="Employee ID" className="w-full text-sm border p-2 rounded" />
                                    <input type="text" name="employee_name" value={config.employee_name} onChange={handleChange} placeholder="Name" className="w-full text-sm border p-2 rounded" />
                                    <select name="billable" value={config.billable} onChange={handleChange} className="w-full text-sm border p-2 rounded">
                                        <option value="Yes">Billable: Yes</option>
                                        <option value="No">Billable: No</option>
                                    </select>
                                </div>
                            </div>

                            <button
                                onClick={generateTimesheet}
                                disabled={loading}
                                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                            >
                                {loading ? 'Generating...' : 'Generate Timesheet'}
                            </button>
                        </div>
                    </div>

                    {/* Main Content */}
                    <div className="md:col-span-3 bg-white p-6 rounded-lg shadow-sm overflow-hidden">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-lg font-semibold">Generated Entries</h2>
                            {entries.length > 0 && (
                                <button onClick={downloadCSV} className="text-sm bg-green-600 text-white px-3 py-1.5 rounded hover:bg-green-700 shadow-sm transition-colors">
                                    Download CSV
                                </button>
                            )}
                        </div>

                        {entries.length === 0 ? (
                            <p>Click &quot;Generate Timesheet&quot; to fetch data from Jira and GitHub.</p>
                        ) : (
                            <div className="overflow-x-auto">
                                <table className="min-w-full divide-y divide-gray-200 border">
                                    <thead className="bg-gray-50">
                                        <tr>
                                            <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">Date</th>
                                            <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">Project</th>
                                            <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-48">Task</th>
                                            <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-64">Description</th>
                                            <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">Status</th>
                                            <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Remark (Editable)</th>
                                            <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-16">Hrs</th>
                                        </tr>
                                    </thead>
                                    <tbody className="bg-white divide-y divide-gray-200">
                                        {entries.map((entry, idx) => (
                                            <tr key={idx} className="hover:bg-gray-50 transition-colors">
                                                <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-500">{entry.date}</td>
                                                <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-900">{entry.project}</td>
                                                <td className="px-3 py-2 text-sm text-gray-900">
                                                    <input
                                                        value={entry.task}
                                                        onChange={(e) => handleEntryChange(idx, 'task', e.target.value)}
                                                        className="w-full border-gray-300 rounded text-sm focus:ring-blue-500 focus:border-blue-500 p-1 border"
                                                    />
                                                </td>
                                                <td className="px-3 py-2 text-sm text-gray-900">
                                                    <textarea
                                                        value={entry.task_description}
                                                        onChange={(e) => handleEntryChange(idx, 'task_description', e.target.value)}
                                                        className="w-full border-gray-300 rounded text-sm focus:ring-blue-500 focus:border-blue-500 p-1 border h-20 resize-none"
                                                    />
                                                </td>
                                                <td className="px-3 py-2 whitespace-nowrap text-sm">
                                                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${entry.status === 'Done' || entry.status === 'Completed' ? 'bg-green-100 text-green-800' :
                                                        entry.status === 'In Progress' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'
                                                        }`}>
                                                        {entry.status}
                                                    </span>
                                                </td>
                                                <td className="px-3 py-2 text-sm text-gray-500">
                                                    <textarea
                                                        value={entry.remark}
                                                        onChange={(e) => handleEntryChange(idx, 'remark', e.target.value)}
                                                        className="w-full border-gray-300 rounded text-sm focus:ring-blue-500 focus:border-blue-500 p-1 border h-20"
                                                    />
                                                </td>
                                                <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-500">
                                                    <input
                                                        value={entry.hours}
                                                        onChange={(e) => handleEntryChange(idx, 'hours', e.target.value)}
                                                        className="w-12 border-gray-300 rounded text-sm focus:ring-blue-500 focus:border-blue-500 p-1 border text-center"
                                                    />
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
